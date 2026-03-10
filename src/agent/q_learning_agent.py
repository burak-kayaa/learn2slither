from dataclasses import dataclass, field
import random

from src.config import ACTIONS, Direction



@dataclass
class QLearningAgent:
    q_table: dict[tuple, dict[str, float]]
    epsilom: float = 0.1

    def ensure_state_exists(self, state_key: tuple) -> None:
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in ACTIONS}

    def get_action_values(self, state_key: tuple) -> dict[str, float]:
        self.ensure_state_exists(state_key)
        return self.q_table[state_key]
    
    def best_action(self, state_key: tuple) -> str:
        action_values = self.get_action_values(state_key)
        max_value = max(action_values.values())
        best_actions = [action for action, value in action_values.items() if value == max_value]
        return random.choice(best_actions)
    
    def select_action(self, state_key: tuple) -> str:
        if random.random() < self.epsilom:
            return random.choice(ACTIONS)
        else:
            return self.best_action(state_key)