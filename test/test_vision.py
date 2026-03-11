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
    vision = VisionInterpreter.extract(game)
    assert vision["UP"] == "SNAKE"        # (2,1) snake body — duvardan önce bulunur
    assert vision["DOWN"] == "RED_APPLE"  # (2,3) red apple
    assert vision["LEFT"] == "WALL"       # (1,2),(0,2) boş → (−1,2) dışarı → WALL
    assert vision["RIGHT"] == "GREEN_APPLE"  # (3,2) green apple


def test_vision_empty():
    game = Game(width=5, height=5)
    game.snake = Snake([(0, 0)])
    game.green_apples = []
    game.red_apple = (4, 4)
    vision = VisionInterpreter.extract(game)
    assert vision["UP"] == "WALL"    # hemen dışarı
    assert vision["DOWN"] == "WALL"  # (0,1)(0,2)(0,3)(0,4) boş → (0,5) dışarı
    assert vision["LEFT"] == "WALL"  # hemen dışarı
    assert vision["RIGHT"] == "WALL" # (1,0)..(4,0) boş → (5,0) dışarı