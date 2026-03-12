"""Run screen: live board + stats panel during training / evaluation."""

from __future__ import annotations

import threading
import pygame

from src.ui import theme
from src.ui.screen_manager import Screen, ScreenManager
from src.ui.widgets import (
    draw_text, draw_panel, draw_stat_row,
)
from src.environment.game import Game
from src.agent.q_learning_agent import QLearningAgent
from src.agent.reward import compute_reward
from src.state.vision import VisionInterpreter
from src.state.encoder import StateEncoder
from src.config import (
    BOARD_WIDTH, BOARD_HEIGHT,
    EpisodeMetrics, Event,
    RELATIVE_ACTIONS, RELATIVE_TO_ABSOLUTE,
    MAX_STEPS_PER_EPISODE, LOOP_WINDOW, RewardConfig,
    REASON_LABELS,
)
import time
from collections import deque


class RunScreen(Screen):
    def __init__(self, manager: ScreenManager, app_config: dict) -> None:
        super().__init__(manager)
        self.cfg = app_config
        self.env = Game()
        self.agent: QLearningAgent | None = None
        self.all_metrics: list[EpisodeMetrics] = []
        self.episode = 0
        self.step = 0
        self.total_reward = 0.0
        self.current_length = 3
        self.max_length = 3
        self.green_eaten = 0
        self.red_eaten = 0
        self.last_event = ""
        self.death_reason = ""
        self.paused = False
        self.step_mode: bool = app_config.get("step_mode", False)
        self.waiting_step = False
        self.delay_ms: int = app_config.get("delay_ms", 1)
        self.finished = False
        self._worker: threading.Thread | None = None
        self._stop = threading.Event()
        self._step_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.set()

    # ── lifecycle ─────────────────────────────────────────────────────
    def _start_worker(self) -> None:
        self._worker = threading.Thread(target=self._run_training, daemon=True)
        self._worker.start()

    def _build_agent(self) -> QLearningAgent:
        cfg = self.cfg
        if cfg.get("mode") == "evaluate" and cfg.get("load_path"):
            agent = QLearningAgent.load(cfg["load_path"])
        else:
            agent = QLearningAgent(
                alpha=cfg.get("alpha", 0.1),
                gamma=cfg.get("gamma", 0.9),
                epsilon=cfg.get("epsilon", 1.0),
                epsilon_decay=cfg.get("epsilon_decay", 0.9997),
                epsilon_min=cfg.get("epsilon_min", 0.05),
            )
        if cfg.get("dont_learn"):
            agent.learning_enabled = False
        return agent

    def _run_training(self) -> None:
        self.agent = self._build_agent()
        sessions = self.cfg.get("sessions", 1000)
        if self.agent.epsilon > self.agent.epsilon_min:
            exploit_start = max(1, int(sessions * 0.8))
            self.agent.epsilon_decay = (
                self.agent.epsilon_min / self.agent.epsilon
            ) ** (1.0 / exploit_start)
        for ep in range(1, sessions + 1):
            if self._stop.is_set():
                break
            metrics = self._run_single_episode(ep)
            self.all_metrics.append(metrics)
            self.agent.decay_epsilon()

        self.finished = True

    def _run_single_episode(self, episode_index: int) -> EpisodeMetrics:
        self.env.reset()
        self.episode = episode_index
        self.step = 0
        self.total_reward = 0.0
        self.green_eaten = 0
        self.red_eaten = 0
        self.max_length = len(self.env.snake)
        self.death_reason = ""
        start = time.perf_counter()
        done = False
        death_reason = None
        visited: deque = deque(maxlen=LOOP_WINDOW)
        while not done and not self._stop.is_set():
            self._pause_event.wait()
            if self.step_mode or self.waiting_step:
                self.waiting_step = True
                self._step_event.clear()
                self._step_event.wait()
            vision = VisionInterpreter.extract(self.env)
            state_key = StateEncoder.encode(
                vision, self.env.snake.direction,
            )
            rel = self.agent.select_action(state_key, RELATIVE_ACTIONS)
            abs_action = RELATIVE_TO_ABSOLUTE[self.env.snake.direction][rel]
            step_result = self.env.step(abs_action)
            reward = compute_reward(step_result)
            if not step_result.done and len(self.env.snake) > 0:
                if self.env.snake.head in visited:
                    reward += RewardConfig.loop_penalty
                visited.append(self.env.snake.head)
            self.step += 1
            self.total_reward += reward
            self.current_length = len(self.env.snake)
            self.last_event = step_result.event.value
            if step_result.event == Event.GREEN_APPLE:
                self.green_eaten += 1
                visited.clear()
            elif step_result.event == Event.RED_APPLE:
                self.red_eaten += 1
            self.max_length = max(self.max_length, len(self.env.snake))
            if step_result.done:
                death_reason = step_result.event
                self.death_reason = REASON_LABELS.get(
                    step_result.event, str(step_result.event),
                )
                next_state_key = state_key
            else:
                next_vis = VisionInterpreter.extract(self.env)
                next_state_key = StateEncoder.encode(
                    next_vis, self.env.snake.direction,
                )
            self.agent.learn(
                state_key=state_key,
                action=rel,
                reward=reward,
                next_state_key=next_state_key,
                done=step_result.done,
                valid_next_actions=RELATIVE_ACTIONS,
            )
            done = step_result.done
            if not done and self.step >= MAX_STEPS_PER_EPISODE:
                death_reason = Event.MAX_STEPS
                self.death_reason = "Max Steps"
                done = True
            if self.delay_ms > 0 and not self.step_mode:
                time.sleep(self.delay_ms / 1000.0)
        elapsed = time.perf_counter() - start
        return EpisodeMetrics(
            episode_index=episode_index,
            steps=self.step,
            duration_seconds=elapsed,
            total_reward=self.total_reward,
            final_length=len(self.env.snake),
            max_length=self.max_length,
            green_apples_eaten=self.green_eaten,
            red_apples_eaten=self.red_eaten,
            death_reason=death_reason,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_SPACE:
            self.paused = not self.paused
            if self.paused:
                self._pause_event.clear()
            else:
                self._pause_event.set()
        elif event.key == pygame.K_n:
            self._step_event.set()
        elif event.key == pygame.K_s and self.agent:
            self.agent.save(self.cfg.get("sessions", 0))
        elif event.key == pygame.K_ESCAPE:
            self._stop.set()
            self._pause_event.set()
            self._step_event.set()
            if self.finished or self._stop.is_set():
                self._go_to_results()

    def _go_to_results(self) -> None:
        from src.ui.screens.results_screen import ResultsScreen
        self.manager.replace(
            ResultsScreen(
                self.manager, self.cfg, self.all_metrics, self.agent
            ),
        )

    def update(self) -> None:
        if self._worker is None:
            self._start_worker()
        if self.finished:
            self._go_to_results()

    def draw(self, surface: pygame.Surface) -> None:
        self._draw_board(surface)
        self._draw_side_panel(surface)

    def _draw_board(self, surface: pygame.Surface) -> None:
        bx = theme.BOARD_OFFSET_X
        by = theme.BOARD_OFFSET_Y
        cs = theme.CELL_SIZE
        # border
        border_rect = pygame.Rect(bx - 2, by - 2,
                                  BOARD_WIDTH * cs + 4,
                                  BOARD_HEIGHT * cs + 4)
        pygame.draw.rect(surface, theme.PANEL_BORDER, border_rect,
                         width=2, border_radius=4)

        # cells
        for cy in range(BOARD_HEIGHT):
            for cx in range(BOARD_WIDTH):
                rect = pygame.Rect(bx + cx * cs, by + cy * cs, cs, cs)
                pygame.draw.rect(surface, theme.EMPTY_CELL, rect)
                pygame.draw.rect(surface, theme.GRID_LINE, rect, 1)

        # apples
        for ax, ay in self.env.green_apples:
            r = pygame.Rect(
                bx + ax * cs + 3, by + ay * cs + 3, cs - 6, cs - 6
            )
            pygame.draw.rect(surface, theme.GREEN_APPLE, r, border_radius=8)
        if self.env.red_apple:
            rx, ry = self.env.red_apple
            r = pygame.Rect(
                bx + rx * cs + 3, by + ry * cs + 3, cs - 6, cs - 6
            )
            pygame.draw.rect(surface, theme.RED_APPLE, r, border_radius=8)

        # snake
        snake_list = self.env.snake.as_list()
        for i, (sx, sy) in enumerate(snake_list):
            color = theme.SNAKE_HEAD if i == 0 else theme.SNAKE_BODY
            r = pygame.Rect(
                bx + sx * cs + 2, by + sy * cs + 2, cs - 4, cs - 4
            )
            pygame.draw.rect(
                surface, color, r,
                border_radius=6 if i == 0 else 3,
            )

        # title above board
        mode = self.cfg.get("mode", "train").title()
        draw_text(
            surface, f"Mode: {mode}", bx, 20, theme.ACCENT, 20, bold=True,
        )
        status = (
            "PAUSED" if self.paused
            else ("STEP" if self.step_mode else "RUNNING")
        )
        draw_text(
            surface, status, bx + 300, 20,
            theme.WARNING if self.paused else theme.SUCCESS, 18, bold=True,
        )

    def _draw_side_panel(self, surface: pygame.Surface) -> None:
        px = theme.BOARD_AREA_W + 8
        pw = theme.SIDE_PANEL_W - 24
        panel_rect = pygame.Rect(px, 20, pw, theme.WINDOW_H - 40)
        draw_panel(surface, panel_rect)

        x = px + theme.PAD
        y = 40
        stat_w = pw - theme.PAD * 2

        y = draw_stat_row(surface, x, y, "Episode", str(self.episode), stat_w)
        y = draw_stat_row(surface, x, y, "Step", str(self.step), stat_w)
        y = draw_stat_row(
            surface, x, y, "Total Reward",
            f"{self.total_reward:.1f}", stat_w,
        )
        eps_str = f"{self.agent.epsilon:.4f}" if self.agent else "-"
        y = draw_stat_row(surface, x, y, "Epsilon", eps_str, stat_w)
        y += 8

        y = draw_stat_row(
            surface, x, y, "Snake Length",
            str(self.current_length), stat_w,
            value_color=theme.ACCENT,
        )
        y = draw_stat_row(
            surface, x, y, "Max Length", str(self.max_length), stat_w,
        )
        y = draw_stat_row(
            surface, x, y, "Green Eaten", str(self.green_eaten), stat_w,
            value_color=theme.GREEN_APPLE,
        )
        y = draw_stat_row(
            surface, x, y, "Red Eaten", str(self.red_eaten), stat_w,
            value_color=theme.RED_APPLE,
        )
        y += 8

        y = draw_stat_row(
            surface, x, y, "Last Event", self.last_event, stat_w,
        )
        y = draw_stat_row(
            surface, x, y, "Death Reason",
            self.death_reason or "-", stat_w,
            value_color=(
                theme.DANGER if self.death_reason else theme.TEXT_DIM
            ),
        )
        y += 8

        qtable_size = len(self.agent.q_table) if self.agent else 0
        y = draw_stat_row(
            surface, x, y, "Q-Table Size", str(qtable_size), stat_w,
        )
        total_sessions = self.cfg.get("sessions", 0)
        y = draw_stat_row(
            surface, x, y, "Sessions",
            f"{self.episode}/{total_sessions}", stat_w,
        )
        y = draw_stat_row(
            surface, x, y, "Delay (ms)", str(self.delay_ms), stat_w,
        )
        y += 16

        # progress bar
        if total_sessions > 0:
            pct = min(self.episode / total_sessions, 1.0)
            bar_bg = pygame.Rect(x, y, stat_w, 14)
            bar_fg = pygame.Rect(x, y, int(stat_w * pct), 14)
            pygame.draw.rect(
                surface, theme.PANEL_BORDER, bar_bg, border_radius=4,
            )
            if pct > 0:
                pygame.draw.rect(
                    surface, theme.ACCENT, bar_fg, border_radius=4,
                )
            draw_text(
                surface, f"{pct*100:.0f}%",
                x + stat_w // 2, y - 1, theme.TEXT, 12,
                anchor="midtop",
            )
            y += 28

        # controls hint
        y = theme.WINDOW_H - 120
        draw_text(surface, "Controls:", x, y, theme.TEXT_DIM, 14, bold=True)
        y += 20
        for hint in [
            "SPACE  Pause/Resume",
            "N      Next Step",
            "S      Save Model",
            "ESC    Stop & Results",
        ]:
            draw_text(surface, hint, x, y, theme.TEXT_DIM, 13)
            y += 18
