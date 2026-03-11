from src.environment.board import Board
from src.environment.game import Game
from src.state.vision import VisionInterpreter
from src.state.encoder import StateEncoder
from src.agent.q_learning_agent import QLearningAgent

from src.agent.reward import compute_reward
from src.config import REASON_LABELS, EpisodeMetrics, Event, RELATIVE_ACTIONS, RELATIVE_TO_ABSOLUTE, MAX_STEPS_PER_EPISODE, LOOP_WINDOW, RewardConfig
import time
from collections import deque
from dataclasses import dataclass

from src.ui.renderer import GameRenderer


def run_episode(env: Game, agent: QLearningAgent, episode_index: int, renderer: GameRenderer | None) -> EpisodeMetrics:
    env.reset()
    start_time = time.perf_counter()
    steps = 0
    total_reward = 0.0
    green_apples_eaten = 0
    red_apples_eaten = 0
    max_length = len(env.snake)
    death_reason = None
    done = False
    visited_positions: deque = deque(maxlen=LOOP_WINDOW)
    while not done:
        vision = VisionInterpreter.extract(env)
        state_key = StateEncoder.encode(vision, env.snake.direction)
        rel_action = agent.select_action(state_key, RELATIVE_ACTIONS)
        abs_action = RELATIVE_TO_ABSOLUTE[env.snake.direction][rel_action]
        if renderer:
            VisionInterpreter.print_cross(env, abs_action)
        step_result = env.step(abs_action)
        reward = compute_reward(step_result)
        if not step_result.done and len(env.snake) > 0:
            if env.snake.head in visited_positions:
                reward += RewardConfig.loop_penalty
            visited_positions.append(env.snake.head)
        steps += 1
        total_reward += reward
        if step_result.event == Event.GREEN_APPLE:
            green_apples_eaten += 1
            visited_positions.clear()
        elif step_result.event == Event.RED_APPLE:
            red_apples_eaten += 1
        max_length = max(max_length, len(env.snake))
        if step_result.done:
            death_reason = step_result.event
            next_state_key = state_key
        else:
            next_vision = VisionInterpreter.extract(env)
            next_state_key = StateEncoder.encode(next_vision, env.snake.direction)
        agent.learn(
            state_key=state_key,
            action=rel_action,
            reward=reward,
            next_state_key=next_state_key,
            done=step_result.done,
            valid_next_actions=RELATIVE_ACTIONS,
        )
        if renderer:
            renderer.render(env)
        done = step_result.done
        if not done and steps >= MAX_STEPS_PER_EPISODE:
            death_reason = REASON_LABELS.get(str(Event.MAX_STEPS), str(Event.MAX_STEPS))
            done = True
    duration_seconds = time.perf_counter() - start_time
    print(f"[Episode {episode_index}] Game Over - Length: {len(env.snake)} - Steps: {steps}")
    return EpisodeMetrics(
        episode_index=episode_index,
        steps=steps,
        duration_seconds=duration_seconds,
        total_reward=total_reward,
        final_length=len(env.snake),
        max_length=max_length,
        green_apples_eaten=green_apples_eaten,
        red_apples_eaten=red_apples_eaten,
        death_reason=death_reason,
    )


def train(env: Game, agent: QLearningAgent, sessions: int, renderer: GameRenderer | None) -> list[EpisodeMetrics]:
    all_metrics = []
    exploit_start = max(1, int(sessions * 0.8))
    if agent.epsilon > agent.epsilon_min:
        agent.epsilon_decay = (agent.epsilon_min / agent.epsilon) ** (1.0 / exploit_start)
    for episode in range(1, sessions + 1):
        metrics = run_episode(
            env=env,
            agent=agent,
            episode_index=episode,
            renderer=renderer
        )
        all_metrics.append(metrics)
        agent.decay_epsilon()
    return all_metrics