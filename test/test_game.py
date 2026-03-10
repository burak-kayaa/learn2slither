import pytest

from src.config import Event
from src.environment.game import Game


def test_game_initialization():
    game = Game(width=10, height=10)
    assert game.board.width == 10
    assert game.board.height == 10
    assert len(game.snake.body) == 3
    assert len(game.green_apples) == 2
    assert game.red_apple is not None
    assert not game.done

    
def test_game_reset():
    game = Game(width=10, height=10)
    game.step("UP")
    game.reset()
    assert len(game.snake.body) == 3
    assert len(game.green_apples) == 2
    assert game.red_apple is not None
    assert not game.done
    

def test_game_step_wall_collision():
    game = Game(width=5, height=5)
    for _ in range(3):
        result = game.step("UP")
    assert result.event == Event.WALL_COLLISION
    assert result.done
    assert game.done
    
    
def test_game_step_self_collision():
    game = Game(width=5, height=5)
    game.red_apple = None
    game.green_apples.clear()
    head_x, head_y = game.snake.head
    green_apple_pos = (head_x, head_y - 1)
    game.green_apples.add(green_apple_pos)
    game.step("UP")
    head_x, head_y = game.snake.head
    green_apple_pos = (head_x, head_y - 1)
    game.green_apples.add(green_apple_pos)
    game.step("UP")
    game.step("LEFT")
    game.step("DOWN")
    result = game.step("RIGHT")
    assert result.event == Event.SNAKE_COLLISION
    assert result.done
    assert game.done
    
    
    
def test_game_step_green_apple():
    game = Game(width=5, height=5)
    head_x, head_y = game.snake.head
    green_apple_pos = (head_x, head_y - 1)
    game.green_apples.add(green_apple_pos)
    result = game.step("UP")
    assert result.event == Event.GREEN_APPLE
    assert not result.done
    assert result.score_delta == 1
    assert len(game.snake.body) == 4
    
    
def test_game_step_red_apple():
    game = Game(width=5, height=5)
    head_x, head_y = game.snake.head
    game.green_apples.clear()
    red_apple_pos = (head_x, head_y - 1)
    game.red_apple = red_apple_pos  
    result = game.step("UP")
    assert result.event == Event.RED_APPLE
    assert not result.done
    assert result.score_delta == -1
    assert len(game.snake.body) == 2
    
    
def test_game_step_zero_length():
    game = Game(width=8, height=8)
    game.green_apples.clear()
    head_x, head_y = game.snake.head
    for _ in range(3):
        head_x, head_y = game.snake.head
        red_apple_pos = (head_x, head_y - 1)
        game.red_apple = red_apple_pos
        result = game.step("UP")
    assert result.event == Event.ZERO_LENGTH
    assert result.done    

    
def test_game_step_after_game_over():
    game = Game(width=5, height=5)
    for _ in range(3):
        game.step("UP")
    assert game.done
    result = game.step("UP")
    assert result.event == Event.GAME_ALREADY_OVER
    assert result.done
    assert result.score_delta == 0