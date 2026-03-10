import pytest

from src.agent.q_learning_agent import QLearningAgent

# from dataclasses import dataclass, field
# import random

# from src.config import ACTIONS, Direction



# @dataclass
# class QLearningAgent:
#     q_table: dict[tuple, dict[str, float]]
#     epsilom: float = 0.1

#     def ensure_state_exists(self, state_key: tuple) -> None:
#         if state_key not in self.q_table:
#             self.q_table[state_key] = {action: 0.0 for action in ACTIONS}

#     def get_action_values(self, state_key: tuple) -> dict[str, float]:
#         self.ensure_state_exists(state_key)
#         return self.q_table[state_key]
    
#     def best_action(self, state_key: tuple) -> str:
#         action_values = self.get_action_values(state_key)
#         max_value = max(action_values.values())
#         best_actions = [action for action, value in action_values.items() if value == max_value]
#         return random.choice(best_actions)
    
#     def select_action(self, state_key: tuple) -> str:
#         if random.random() < self.epsilom:
#             return random.choice(ACTIONS)
#         else:
#             return self.best_action(state_key)


def test_q_learning_agent():
    agent = QLearningAgent(q_table={})
    state_key = (("0", "0"), ("0", "0"), ("0", "0"), ("0", "0"))
    action_values = agent.get_action_values(state_key)
    assert action_values == {"UP": 0.0, "LEFT": 0.0, "DOWN": 0.0, "RIGHT": 0.0}
    best_action = agent.best_action(state_key)
    assert best_action in ["UP", "LEFT", "DOWN", "RIGHT"]
    selected_action = agent.select_action(state_key)
    assert selected_action in ["UP", "LEFT", "DOWN", "RIGHT"]
    
    
def test_q_learning_agent_exploration():
    agent = QLearningAgent(q_table={}, epsilom=1.0)  # Always explore
    state_key = (("0", "0"), ("0", "0"), ("0", "0"), ("0", "0"))
    selected_action = agent.select_action(state_key)
    assert selected_action in ["UP", "LEFT", "DOWN", "RIGHT"]
    
    
def test_q_learning_agent_exploitation():
    agent = QLearningAgent(q_table={}, epsilom=0.0)  # Always exploit
    state_key = (("0", "0"), ("0", "0"), ("0", "0"), ("0", "0"))
    agent.q_table[state_key] = {"UP": 1.0, "LEFT": 0.5, "DOWN": 0.2, "RIGHT": 0.3}
    selected_action = agent.select_action(state_key)
    assert selected_action == "UP"
