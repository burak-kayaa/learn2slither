from src.environment.snake import Snake
from src.environment.game import Game
from src.state.vision import VisionInterpreter


def test_vision_extraction():
    game = Game(width=5, height=5)
    game.snake = Snake([(2, 2), (2, 1), (2, 0)])
    game.green_apples = [(3, 2), (4, 2)]
    game.red_apple = (2, 3)
    vision = VisionInterpreter.extract(game)
    assert vision["UP"] == ("SNAKE", "CLOSE")         # (2,1) dist=1 → CLOSE
    assert vision["DOWN"] == ("RED_APPLE", "CLOSE")   # (2,3) dist=1 → CLOSE
    assert vision["LEFT"] == ("WALL", "NEAR")  # wall at (-1,2), dist=3 → NEAR
    assert vision["RIGHT"] == ("GREEN_APPLE", "CLOSE")  # (3,2) dist=1 → CLOSE


def test_vision_empty():
    game = Game(width=5, height=5)
    game.snake = Snake([(0, 0)])
    game.green_apples = []
    game.red_apple = (4, 4)
    vision = VisionInterpreter.extract(game)
    assert vision["UP"] == ("WALL", "CLOSE")    # (0,-1) dist=1
    assert vision["DOWN"] == ("WALL", "FAR")    # (0,5) dist=5
    assert vision["LEFT"] == ("WALL", "CLOSE")  # (-1,0) dist=1
    assert vision["RIGHT"] == ("WALL", "FAR")   # (5,0) dist=5
