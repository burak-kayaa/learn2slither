import pytest

from src.state.encoder import StateEncoder


def test_state_encoder():
    vision = {
        "UP": ["0", "S", "G"],
        "DOWN": ["R", "0", "0"],
        "LEFT": ["W", "S", "0"],
        "RIGHT": ["0", "0", "G"],
    }
    expected = (
        ("0", "S", "G"),
        ("R", "0", "0"),
        ("W", "S", "0"),
        ("0", "0", "G"),
    )
    assert StateEncoder.encode(vision) == expected