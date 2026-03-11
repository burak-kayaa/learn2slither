"""Configuration constants for the Snake game."""

from dataclasses import dataclass
from enum import Enum


BOARD_WIDTH: int = 10
BOARD_HEIGHT: int = 10
INITIAL_SNAKE_LENGTH: int = 3
GREEN_APPLE_COUNT: int = 2
RED_APPLE_COUNT: int = 1

MAX_STEPS_PER_EPISODE: int = BOARD_WIDTH * BOARD_HEIGHT * 4
LOOP_WINDOW: int = 20

MODEL_SAVE_PATH_SRC: str = "./models"

@dataclass
class StepResult:
    event: Event
    done: bool
    score_delta: int = 0

@dataclass(frozen=True)
class RewardConfig:
    green_apple: float = 10.0
    red_apple: float = -8.0
    step: float = -0.4
    game_over: float = -20.0
    loop_penalty: float = -4.0


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

RELATIVE_ACTIONS: list[str] = ["AHEAD", "TURN_LEFT", "TURN_RIGHT"]

RELATIVE_TO_ABSOLUTE: dict[str, dict[str, str]] = {
    Direction.RIGHT: {"AHEAD": Direction.RIGHT, "TURN_LEFT": Direction.UP,   "TURN_RIGHT": Direction.DOWN},
    Direction.LEFT:  {"AHEAD": Direction.LEFT,  "TURN_LEFT": Direction.DOWN, "TURN_RIGHT": Direction.UP},
    Direction.UP:    {"AHEAD": Direction.UP,    "TURN_LEFT": Direction.LEFT,  "TURN_RIGHT": Direction.RIGHT},
    Direction.DOWN:  {"AHEAD": Direction.DOWN,  "TURN_LEFT": Direction.RIGHT, "TURN_RIGHT": Direction.LEFT},
}

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
    MAX_STEPS = "MAX_STEPS"
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

class Colors:
    BACKGROUND = (20, 20, 20)
    GRID = (60, 60, 60)
    SNAKE = (50, 120, 255)
    GREEN_APPLE = (0, 200, 0)
    RED_APPLE = (220, 40, 40)
    
REASON_LABELS = {
    Event.WALL_COLLISION: "Wall Collision",
    Event.SELF_COLLISION: "Self Collision",
    Event.ZERO_LENGTH: "Zero Length",
    Event.MAX_STEPS: "Max Steps",
}