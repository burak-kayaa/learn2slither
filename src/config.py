"""Configuration constants for the Snake game.
"""

UP: str = "UP"
LEFT: str = "LEFT"
DOWN: str = "DOWN"
RIGHT: str = "RIGHT"
BOARD_WIDTH: int = 10
BOARD_HEIGHT: int = 10
INITIAL_SNAKE_LENGTH: int = 3
GREEN_APPLE_COUNT: int = 2
RED_APPLE_COUNT: int = 1
ACTIONS: list[str] = [UP, LEFT, DOWN, RIGHT]

class Direction:
    UP = UP
    LEFT = LEFT
    DOWN = DOWN
    RIGHT = RIGHT