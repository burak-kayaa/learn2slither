import pytest

from src.environment.board import Board
from src.environment.game import Position
from src.environment.snake import Snake
from src.environment.apples import AppleManager

def test_spawn_initial_apples() -> None:
    board = Board(width=10, height=10)
    snake = Snake.create_default(board_width=10, board_height=10)

    green_apples, red_apple = AppleManager.spawn_initial(board, snake)

    assert len(green_apples) == AppleManager.GREEN_COUNT
    assert red_apple not in green_apples
    assert red_apple not in snake.as_list()
    for apple in green_apples:
        assert apple not in snake.as_list()
        

def test_spawn_green_apple() -> None:
    board = Board(width=10, height=10)
    snake = Snake.create_default(board_width=10, board_height=10)
    green_apples, red_apple = AppleManager.spawn_initial(board, snake)

    new_green_apple = AppleManager.spawn_green(board, snake, green_apples, red_apple)

    assert new_green_apple not in green_apples
    assert new_green_apple != red_apple
    assert new_green_apple not in snake.as_list()
    

def test_spawn_red_apple() -> None:
    board = Board(width=10, height=10)
    snake = Snake.create_default(board_width=10, board_height=10)
    green_apples, _ = AppleManager.spawn_initial(board, snake)

    new_red_apple = AppleManager.spawn_red(board, snake, green_apples)

    assert new_red_apple not in green_apples
    assert new_red_apple not in snake.as_list()
    