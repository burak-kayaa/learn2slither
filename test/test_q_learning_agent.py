import pytest

from src.agent.q_learning_agent import QLearningAgent
from src.config import RELATIVE_ACTIONS

import random


REL = RELATIVE_ACTIONS  # ["AHEAD", "TURN_LEFT", "TURN_RIGHT"]


def test_q_learning_agent():
    agent = QLearningAgent(q_table={})
    state_key = ("WALL", "EMPTY", "GREEN_APPLE")
    action_values = agent.get_action_values(state_key)
    assert action_values == {"AHEAD": 0.0, "TURN_LEFT": 0.0, "TURN_RIGHT": 0.0}
    best_action = agent.best_action(state_key)
    assert best_action in REL
    selected_action = agent.select_action(state_key, REL)
    assert selected_action in REL


def test_q_learning_agent_exploration():
    agent = QLearningAgent(q_table={}, epsilon=1.0)
    state_key = ("WALL", "EMPTY", "GREEN_APPLE")
    selected_action = agent.select_action(state_key, REL)
    assert selected_action in REL


def test_q_learning_agent_exploitation():
    agent = QLearningAgent(q_table={}, epsilon=0.0)
    state_key = ("WALL", "EMPTY", "GREEN_APPLE")
    agent.q_table[state_key] = {"AHEAD": 0.2, "TURN_LEFT": 1.0, "TURN_RIGHT": 0.5}
    selected_action = agent.select_action(state_key, REL)
    assert selected_action == "TURN_LEFT"


def test_q_learning_agent_learning():
    agent = QLearningAgent(q_table={}, alpha=0.5, gamma=0.9)
    state_key = ("WALL", "EMPTY", "GREEN_APPLE")
    next_state_key = ("EMPTY", "WALL", "SNAKE")
    agent.q_table[next_state_key] = {"AHEAD": 2.0, "TURN_LEFT": 1.0, "TURN_RIGHT": 0.5}
    agent.learn(state_key, "TURN_LEFT", reward=1.0, next_state_key=next_state_key, done=False)
    expected_value = 0.5 * (1.0 + 0.9 * 2.0)
    assert agent.q_table[state_key]["TURN_LEFT"] == expected_value


def test_q_learning_agent_learning_done():
    agent = QLearningAgent(q_table={}, alpha=0.5, gamma=0.9)
    state_key = ("WALL", "EMPTY", "GREEN_APPLE")
    agent.learn(state_key, "AHEAD", reward=1.0, next_state_key=None, done=True)
    expected_value = 0.5 * 1.0
    assert agent.q_table[state_key]["AHEAD"] == expected_value


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
    state_key = ("WALL", "EMPTY", "GREEN_APPLE")
    next_state_key = ("EMPTY", "WALL", "SNAKE")
    agent.q_table[next_state_key] = {"AHEAD": 2.0, "TURN_LEFT": 1.0, "TURN_RIGHT": 0.5}
    agent.learn(state_key, "AHEAD", reward=1.0, next_state_key=next_state_key, done=False)
    assert state_key not in agent.q_table


def test_q_learning_agent_epsilon_decay_disabled():
    agent = QLearningAgent(q_table={}, learning_enabled=False, epsilon=1.0, epsilon_decay=0.5, epsilon_min=0.1)
    agent.decay_epsilon()
    assert agent.epsilon == 1.0