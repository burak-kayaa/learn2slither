import pytest

from src.state.encoder import StateEncoder


def test_state_encoder_facing_right():
    # Facing RIGHT: ahead=RIGHT, rel_left=UP, rel_right=DOWN
    vision = {
        "UP": "WALL",
        "DOWN": "GREEN_APPLE",
        "LEFT": "SNAKE",
        "RIGHT": "EMPTY",
    }
    # ahead=EMPTY, rel_left=WALL, rel_right=GREEN_APPLE
    assert StateEncoder.encode(vision, "RIGHT") == ("EMPTY", "WALL", "GREEN_APPLE")


def test_state_encoder_facing_up():
    # Facing UP: ahead=UP, rel_left=LEFT, rel_right=RIGHT
    vision = {
        "UP": "GREEN_APPLE",
        "DOWN": "SNAKE",
        "LEFT": "WALL",
        "RIGHT": "EMPTY",
    }
    # ahead=GREEN_APPLE, rel_left=WALL, rel_right=EMPTY
    assert StateEncoder.encode(vision, "UP") == ("GREEN_APPLE", "WALL", "EMPTY")


def test_state_encoder_facing_down():
    # Facing DOWN: ahead=DOWN, rel_left=RIGHT, rel_right=LEFT
    vision = {
        "UP": "WALL",
        "DOWN": "GREEN_APPLE",
        "LEFT": "EMPTY",
        "RIGHT": "SNAKE",
    }
    # ahead=GREEN_APPLE, rel_left=SNAKE, rel_right=EMPTY
    assert StateEncoder.encode(vision, "DOWN") == ("GREEN_APPLE", "SNAKE", "EMPTY")