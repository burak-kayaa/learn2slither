"""Results / statistics screen shown after training or evaluation."""

from __future__ import annotations

from collections import Counter

import pygame
from src.ui import theme
from src.ui.screen_manager import Screen, ScreenManager
from src.ui.widgets import (
    draw_text, draw_text_centered, draw_panel,
    draw_stat_row, draw_bar_chart, draw_comparison_bars,
)
from src.config import EpisodeMetrics, REASON_LABELS
from src.agent.q_learning_agent import QLearningAgent


class ResultsScreen(Screen):
    def __init__(
        self,
        manager: ScreenManager,
        app_config: dict,
        metrics: list[EpisodeMetrics],
        agent: QLearningAgent | None,
    ) -> None:
        super().__init__(manager)
        self.cfg = app_config
        self.metrics = metrics
        self.agent = agent
        self.scroll_y = 0
        self._precompute()

    def _precompute(self) -> None:
        m = self.metrics
        n = len(m) or 1
        self.total_episodes = len(m)
        self.avg_reward = sum(e.total_reward for e in m) / n
        self.best_reward = max((e.total_reward for e in m), default=0)
        self.avg_steps = sum(e.steps for e in m) / n
        self.best_max_len = max((e.max_length for e in m), default=0)
        self.avg_max_len = sum(e.max_length for e in m) / n
        self.total_green = sum(e.green_apples_eaten for e in m)
        self.avg_green = self.total_green / n
        self.total_red = sum(e.red_apples_eaten for e in m)
        self.avg_red = self.total_red / n

        # death reasons
        reasons = Counter(str(e.death_reason) for e in m if e.death_reason)
        self.death_data = [
            (REASON_LABELS.get(k, k).replace("Event.", ""), v)
            for k, v in reasons.most_common()
        ]

        # first/last 100
        first = m[:100] if len(m) >= 100 else m
        last = m[-100:] if len(m) >= 100 else m
        self.cmp_labels = [
            "Avg Steps", "Avg Reward", "Avg MaxLen", "Avg Green",
        ]

        def _avg(lst, attr):
            return sum(getattr(e, attr) for e in lst) / max(len(lst), 1)
        self.cmp_first = [
            _avg(first, "steps"), _avg(first, "total_reward"),
            _avg(first, "max_length"), _avg(first, "green_apples_eaten"),
        ]
        self.cmp_last = [
            _avg(last, "steps"), _avg(last, "total_reward"),
            _avg(last, "max_length"), _avg(last, "green_apples_eaten"),
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.manager.pop()
        elif event.key == pygame.K_UP:
            self.scroll_y = min(self.scroll_y + 40, 0)
        elif event.key == pygame.K_DOWN:
            self.scroll_y -= 40
        elif event.key == pygame.K_s and self.agent:
            self.agent.save(self.cfg.get("sessions", 0))

    def draw(self, surface: pygame.Surface) -> None:
        draw_text_centered(
            surface, "Training Results", 20, theme.ACCENT, 32, bold=True,
        )
        lp = pygame.Rect(24, 70, 580, 680)
        draw_panel(surface, lp)
        x, y = lp.x + 20, lp.y + 16 + self.scroll_y
        w = lp.width - 40
        draw_text(surface, "Summary", x, y, theme.ACCENT, 20, bold=True)
        y += 30
        y = draw_stat_row(
            surface, x, y, "Total Episodes",
            str(self.total_episodes), w,
        )
        y = draw_stat_row(
            surface, x, y, "Avg Reward", f"{self.avg_reward:.2f}", w,
        )
        y = draw_stat_row(
            surface, x, y, "Best Reward", f"{self.best_reward:.2f}", w,
            value_color=theme.SUCCESS,
        )
        y = draw_stat_row(
            surface, x, y, "Avg Steps", f"{self.avg_steps:.1f}", w,
        )
        y = draw_stat_row(
            surface, x, y, "Best Max Length", str(self.best_max_len), w,
            value_color=theme.SUCCESS,
        )
        y = draw_stat_row(
            surface, x, y, "Avg Max Length", f"{self.avg_max_len:.2f}", w,
        )
        y = draw_stat_row(
            surface, x, y, "Green Apples",
            f"{self.total_green}  (avg {self.avg_green:.2f})", w,
            value_color=theme.GREEN_APPLE,
        )
        y = draw_stat_row(
            surface, x, y, "Red Apples",
            f"{self.total_red}  (avg {self.avg_red:.2f})", w,
            value_color=theme.RED_APPLE,
        )
        eps = f"{self.agent.epsilon:.4f}" if self.agent else "-"
        y = draw_stat_row(surface, x, y, "Final Epsilon", eps, w)
        qt = str(len(self.agent.q_table)) if self.agent else "-"
        y = draw_stat_row(surface, x, y, "Q-Table Size", qt, w)
        y += 16
        y = draw_bar_chart(
            surface, x, y, w, 160,
            self.death_data,
            title="Death Reasons",
            bar_color=theme.DANGER,
        )
        rp = pygame.Rect(620, 70, 636, 680)
        draw_panel(surface, rp)
        rx = rp.x + 20
        ry = rp.y + 16 + self.scroll_y
        rw = rp.width - 40
        draw_comparison_bars(
            surface, rx, ry, rw,
            self.cmp_labels, self.cmp_first, self.cmp_last,
            title="First 100 vs Last 100",
        )
        draw_text_centered(
            surface,
            "↑↓  Scroll    S  Save Model    Esc  Back to Lobby",
            theme.WINDOW_H - 30,
            theme.TEXT_DIM, 14,
        )
