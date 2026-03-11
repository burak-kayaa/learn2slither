"""Configuration constants for the Snake game."""

from dataclasses import dataclass
from enum import Enum


BOARD_WIDTH: int = 10
BOARD_HEIGHT: int = 10
INITIAL_SNAKE_LENGTH: int = 3
GREEN_APPLE_COUNT: int = 2
RED_APPLE_COUNT: int = 1


@dataclass
class StepResult:
    event: Event
    done: bool
    score_delta: int = 0

@dataclass(frozen=True)
class RewardConfig:
    green_apple: float = 10.0
    red_apple: float = -8.0
    step: float = -0.1
    game_over: float = -20.0


class Direction:
    UP = "UP"
    LEFT = "LEFT"
    DOWN = "DOWN"
    RIGHT = "RIGHT"


ACTIONS: list[str] = [
    Direction.UP,
    Direction.LEFT,
    Direction.DOWN,
    Direction.RIGHT,
]

DIRECTION_DELTAS: dict[str, tuple[int, int]] = {
    Direction.UP: (0, -1),
    Direction.LEFT: (-1, 0),
    Direction.DOWN: (0, 1),
    Direction.RIGHT: (1, 0),
}


class CellType:
    EMPTY = "0"
    SNAKE = "S"
    GREEN_APPLE = "G"
    RED_APPLE = "R"
    WALL = "W"


class Event(str, Enum):
    GAME_ALREADY_OVER = "GAME_ALREADY_OVER"
    SELF_COLLISION = "SELF_COLLISION"
    WALL_COLLISION = "WALL_COLLISION"
    ZERO_LENGTH = "ZERO_LENGTH"
    GREEN_APPLE = "GREEN_APPLE"
    RED_APPLE = "RED_APPLE"
    MOVE = "MOVE"
    
class EpisodeStats:
    def __init__(self, steps: int, total_reward: float, score: int):
        self.steps = steps
        self.total_reward = total_reward
        self.score = score
        
OPPOSITE_DIRECTIONS = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}