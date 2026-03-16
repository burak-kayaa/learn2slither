from src.config import Event
from src.environment.game import Game
from src.environment.snake import Snake


def _set_snake(game: Game, body: list[tuple[int, int]]) -> None:
    game.snake = Snake(body)


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
    game = Game(width=10, height=10)
    _set_snake(game, [(5, 1), (4, 1), (3, 1)])
    game.green_apples.clear()
    game.red_apple = None
    game.step("UP")
    result = game.step("UP")
    assert result.event == Event.WALL_COLLISION
    assert result.done
    assert game.done


def test_game_step_self_collision():
    game = Game(width=10, height=10)
    _set_snake(game, [(2, 2), (2, 3), (3, 3), (3, 2)])
    game.red_apple = None
    game.green_apples.clear()
    result = game.step("DOWN")
    assert result.event == Event.SELF_COLLISION
    assert result.done
    assert game.done


def test_game_step_green_apple():
    game = Game(width=10, height=10)
    _set_snake(game, [(5, 5), (4, 5), (3, 5)])
    game.green_apples.clear()
    game.red_apple = None
    green_apple_pos = game.get_next_head("UP")
    game.green_apples.add(green_apple_pos)
    result = game.step("UP")
    assert result.event == Event.GREEN_APPLE
    assert not result.done
    assert result.score_delta == 1
    assert len(game.snake.body) == 4


def test_game_step_red_apple():
    game = Game(width=10, height=10)
    _set_snake(game, [(5, 5), (4, 5), (3, 5)])
    game.green_apples.clear()
    red_apple_pos = game.get_next_head("UP")
    game.red_apple = red_apple_pos
    result = game.step("UP")
    assert result.event == Event.RED_APPLE
    assert not result.done
    assert result.score_delta == -1
    assert len(game.snake.body) == 2


def test_game_step_zero_length():
    game = Game(width=10, height=10)
    _set_snake(game, [(5, 5), (4, 5), (3, 5)])
    game.green_apples.clear()
    for _ in range(3):
        red_apple_pos = game.get_next_head("UP")
        game.red_apple = red_apple_pos
        result = game.step("UP")
    assert result.event == Event.ZERO_LENGTH
    assert result.done


def test_game_step_after_game_over():
    game = Game(width=10, height=10)
    _set_snake(game, [(5, 1), (4, 1), (3, 1)])
    game.green_apples.clear()
    game.red_apple = None
    game.step("UP")
    game.step("UP")
    assert game.done
    result = game.step("UP")
    assert result.event == Event.GAME_ALREADY_OVER
    assert result.done
    assert result.score_delta == 0
