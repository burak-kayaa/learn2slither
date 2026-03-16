"""Board class for the Snake game."""

import random
from src.config import BOARD_HEIGHT, BOARD_WIDTH
from typing import Iterable

Position = tuple[int, int]


class Board:
    def __init__(self, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT):
        if width < 10 or height < 10:
            raise ValueError("Board dimensions must be at least 10x10")
        self.width = width
        self.height = height

    def is_inside(self, pos: Position) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def all_positions(self) -> list[Position]:
        return [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
        ]

    def empty_positions(self, occupied: Iterable[Position]) -> list[Position]:
        occupied_set = set(occupied)
        return [pos for pos in self.all_positions() if pos not in occupied_set]

    def random_empty_cell(self, occupied: Iterable[Position]) -> Position:
        empty = self.empty_positions(occupied)
        if not empty:
            raise ValueError("No empty cells available")
        return random.choice(empty)
