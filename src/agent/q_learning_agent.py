from dataclasses import dataclass, field
import random

from src.config import RELATIVE_ACTIONS


@dataclass
class QLearningAgent:
    alpha: float = 0.1
    gamma: float = 0.9
    epsilon: float = 1.0
    epsilon_min: float = 0.05
    epsilon_decay: float = 0.9997
    learning_enabled: bool = True
    q_table: dict[tuple, dict[str, float]] = field(default_factory=dict)

    def ensure_state_exists(self, state_key: tuple) -> None:
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in RELATIVE_ACTIONS}

    def get_action_values(self, state_key: tuple) -> dict[str, float]:
        self.ensure_state_exists(state_key)
        return self.q_table[state_key]

    def best_action(self, state_key: tuple) -> str:
        action_values = self.get_action_values(state_key)
        max_value = max(action_values.values())
        best_actions = [a for a, v in action_values.items() if v == max_value]
        return random.choice(best_actions)

    def select_action(self, state_key: tuple, valid_actions: list[str]) -> str:
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        action_values = self.get_action_values(state_key)
        valid_q = {a: action_values[a] for a in valid_actions}
        max_val = max(valid_q.values())
        return random.choice([a for a, v in valid_q.items() if v == max_val])

    def learn(self, state_key: tuple, action: str, reward: float, next_state_key: tuple, done: bool, valid_next_actions: list[str] | None = None) -> None:
        if not self.learning_enabled:
            return
        if done:
            target = reward
        else:
            next_action_values = self.get_action_values(next_state_key)
            if valid_next_actions:
                max_next_value = max(next_action_values[a] for a in valid_next_actions)
            else:
                max_next_value = max(next_action_values.values())
            target = reward + self.gamma * max_next_value
        current_value = self.get_action_values(state_key)[action]
        new_value = current_value + self.alpha * (target - current_value)
        self.q_table[state_key][action] = new_value

    def decay_epsilon(self) -> None:
        if not self.learning_enabled:
            return
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)