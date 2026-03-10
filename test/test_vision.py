import pytest

from src.environment.snake import Snake
from src.environment.board import Board
from src.environment.game import Game
from src.state.vision import VisionInterpreter

def test_vision_extraction():
    game = Game(width=5, height=5)
    game.snake = Snake([(2, 2), (2, 1), (2, 0)])
    game.green_apples = [(3, 2), (4, 2)]
    game.red_apple = (2, 3)
    print(game.board.print_board(game.snake.as_list(), game.green_apples, game.red_apple))
    vision = VisionInterpreter.extract(game)
    assert vision["UP"] == ["SNAKE", "SNAKE", "WALL"]
    assert vision["DOWN"] == ["RED_APPLE", "EMPTY", "WALL"]
    assert vision["LEFT"] == ["EMPTY", "EMPTY", "WALL"]
    assert vision["RIGHT"] == ["GREEN_APPLE", "GREEN_APPLE", "WALL"]
    
    
def test_vision_empty():
    game = Game(width=5, height=5)
    game.snake = Snake([(0, 0)])
    game.green_apples = []
    game.red_apple = (4, 4)
    print(game.board.print_board(game.snake.as_list(), game.green_apples, game.red_apple))
    vision = VisionInterpreter.extract(game)
    assert vision["UP"] == ["WALL"]
    assert vision["DOWN"] == ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "WALL"]
    assert vision["LEFT"] == ["WALL"]
    assert vision["RIGHT"] == ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "WALL"]