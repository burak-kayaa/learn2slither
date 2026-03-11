from src.environment.board import Board
from src.environment.game import Game
from src.state.vision import VisionInterpreter
from src.state.encoder import StateEncoder
from src.agent.q_learning_agent import QLearningAgent

from src.agent.reward import compute_reward
from src.config import Event, RELATIVE_ACTIONS, RELATIVE_TO_ABSOLUTE
import time
from dataclasses import dataclass


@dataclass
class EpisodeMetrics:
    episode_index: int
    steps: int
    duration_seconds: float
    total_reward: float
    final_length: int
    max_length: int
    green_apples_eaten: int
    red_apples_eaten: int
    death_reason: str | None


def run_episode(env: Game, agent: QLearningAgent, episode_index: int) -> EpisodeMetrics:
    env.reset()
    start_time = time.perf_counter()
    steps = 0
    total_reward = 0.0
    green_apples_eaten = 0
    red_apples_eaten = 0
    max_length = len(env.snake)
    death_reason = None
    done = False
    while not done:
        vision = VisionInterpreter.extract(env)
        state_key = StateEncoder.encode(vision, env.snake.direction)
        rel_action = agent.select_action(state_key, RELATIVE_ACTIONS)
        abs_action = RELATIVE_TO_ABSOLUTE[env.snake.direction][rel_action]
        step_result = env.step(abs_action)
        reward = compute_reward(step_result)
        steps += 1
        total_reward += reward
        if step_result.event == Event.GREEN_APPLE:
            green_apples_eaten += 1
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
        done = step_result.done
    duration_seconds = time.perf_counter() - start_time
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


def train(env: Game, agent: QLearningAgent, sessions: int) -> list[EpisodeMetrics]:
    all_metrics = []
    exploit_start = max(1, int(sessions * 0.8))
    if agent.epsilon > agent.epsilon_min:
        agent.epsilon_decay = (agent.epsilon_min / agent.epsilon) ** (1.0 / exploit_start)
    for episode in range(1, sessions + 1):
        metrics = run_episode(
            env=env,
            agent=agent,
            episode_index=episode,
        )
        all_metrics.append(metrics)
        agent.decay_epsilon()
    return all_metrics