"""Board class for the Snake game."""

import random
from src.config import CellType
from src.config import BOARD_HEIGHT, BOARD_WIDTH
from typing import Iterable

Position = tuple[int, int]


class Board:
    def __init__(self, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT):
        if width <= 0 or height <= 0:
            raise ValueError("Board dimensions must be positive integers")
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
    
    def print_board(self, snake_positions: Iterable[Position], green_apples: Iterable[Position], red_apple: Position) -> None:
        print(CellType.WALL * (self.width + 2))
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                pos = (x, y)
                if pos in snake_positions:
                    row += CellType.SNAKE
                elif pos in green_apples:
                    row += CellType.GREEN_APPLE
                elif pos == red_apple:
                    row += CellType.RED_APPLE
                else:
                    row += CellType.EMPTY
            print(CellType.WALL + row + CellType.WALL)
        print(CellType.WALL * (self.width + 2))