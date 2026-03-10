import pytest

from src.agent.q_learning_agent import QLearningAgent

import random



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
    agent = QLearningAgent(q_table={}, epsilon=1.0)
    state_key = (("0", "0"), ("0", "0"), ("0", "0"), ("0", "0"))
    selected_action = agent.select_action(state_key)
    assert selected_action in ["UP", "LEFT", "DOWN", "RIGHT"]
    
    
def test_q_learning_agent_exploitation():
    agent = QLearningAgent(q_table={}, epsilon=0.0)
    state_key = (("0", "0"), ("0", "0"), ("0", "0"), ("0", "0"))
    agent.q_table[state_key] = {"UP": 1.0, "LEFT": 0.5, "DOWN": 0.2, "RIGHT": 0.3}
    selected_action = agent.select_action(state_key)
    assert selected_action == "UP"


def test_q_learning_agent_learning():
    agent = QLearningAgent(q_table={}, alpha=0.5, gamma=0.9)
    state_key = (("0", "0"), ("0", "0"), ("0", "0"), ("0", "0"))
    next_state_key = (("1", "1"), ("1", "1"), ("1", "1"), ("1", "1"))
    agent.q_table[next_state_key] = {"UP": 2.0, "LEFT": 1.0, "DOWN": 0.5, "RIGHT": 1.5}
    agent.learn(state_key, "UP", reward=1.0, next_state_key=next_state_key, done=False)
    expected_value = 0.5 * (1.0 + 0.9 * 2.0)
    assert agent.q_table[state_key]["UP"] == expected_value
    
    
def test_q_learning_agent_learning_done():
    agent = QLearningAgent(q_table={}, alpha=0.5, gamma=0.9)
    state_key = (("0", "0"), ("0", "0"), ("0", "0"), ("0", "0"))
    agent.learn(state_key, "UP", reward=1.0, next_state_key=None, done=True)
    expected_value = 0.5 * 1.
    assert agent.q_table[state_key]["UP"] == expected_value
    
    
def test_q_learning_agent_epsilon_decay():
    agent = QLearningAgent(q_table={}, epsilon=1.0, epsilon_decay=0.5, epsilon_min=0.1)
    agent.decay_epsilon()
    assert agent.epsilon == 0.5
    agent.decay_epsilon()
    assert agent.epsilon == 0.25
    agent.decay_epsilon()
    assert agent.epsilon == 0.125
    agent.decay_epsilon()
    assert agent.epsilon == 0.1
    

def test_q_learning_agent_learning_disabled():
    agent = QLearningAgent(q_table={}, learning_enabled=False)
    state_key = (("0", "0"), ("0", "0"), ("0", "0"), ("0", "0"))
    next_state_key = (("1", "1"), ("1", "1"), ("1", "1"), ("1", "1"))
    agent.q_table[next_state_key] = {"UP": 2.0, "LEFT": 1.0, "DOWN": 0.5, "RIGHT": 1.5}
    agent.learn(state_key, "UP", reward=1.0, next_state_key=next_state_key, done=False)
    assert state_key not in agent.q_table
    
    
def test_q_learning_agent_epsilon_decay_disabled():
    agent = QLearningAgent(q_table={}, learning_enabled=False, epsilon=1.0, epsilon_decay=0.5, epsilon_min=0.1)
    agent.decay_epsilon()
    assert agent.epsilon == 1.0 