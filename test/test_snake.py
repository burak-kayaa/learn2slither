from src.environment.game import Position
from src.environment.snake import Snake


def test_snake_initialization() -> None:
    initial_body = [
        Position([2, 2]),
        Position([1, 2]),
        Position([0, 2]),
    ]
    snake = Snake(initial_body)

    assert list(snake.body) == initial_body
    assert snake.head == Position([2, 2])
    assert snake.tail == Position([0, 2])


def test_snake_initialization_empty_body() -> None:
    try:
        Snake([])
        assert False, "Expected ValueError for empty initial body"
    except ValueError as e:
        assert str(e) == "Initial body cannot be empty"


def test_snake_moves_right() -> None:
    snake = Snake([
        Position([2, 2]),
        Position([1, 2]),
        Position([0, 2]),
    ])
    snake.move(Position([3, 2]))
    assert list(snake.body) == [
        Position([3, 2]),
        Position([2, 2]),
        Position([1, 2]),
    ]


def test_snake_grows_when_requested() -> None:
    snake = Snake([
        Position([2, 2]),
        Position([1, 2]),
        Position([0, 2]),
    ])
    snake.move(Position([3, 2]), grow=True)
    assert list(snake.body) == [
        Position([3, 2]),
        Position([2, 2]),
        Position([1, 2]),
        Position([0, 2]),
    ]


def test_snake_shrinks() -> None:
    snake = Snake([
        Position([2, 2]),
        Position([1, 2]),
        Position([0, 2]),
    ])
    snake.shrink()
    assert list(snake.body) == [
        Position([2, 2]),
        Position([1, 2]),
    ]
    snake.shrink(2)
    assert list(snake.body) == []


def test_snake_occupies() -> None:
    snake = Snake([
        Position([2, 2]),
        Position([1, 2]),
        Position([0, 2]),
    ])
    assert snake.occupies(Position([2, 2]))
    assert snake.occupies(Position([1, 2]))
    assert snake.occupies(Position([0, 2]))
    assert not snake.occupies(Position([3, 2]))


def test_snake_create_default() -> None:
    snake = Snake.create_default(board_width=10, board_height=10)
    assert list(snake.body) == [
        Position([5, 5]),
        Position([4, 5]),
        Position([3, 5]),
    ]


def test_snake_grows_and_shrinks() -> None:
    snake = Snake([
        Position([2, 2]),
        Position([1, 2]),
        Position([0, 2]),
    ])
    snake.move(Position([3, 2]), grow=True)
    assert list(snake.body) == [
        Position([3, 2]),
        Position([2, 2]),
        Position([1, 2]),
        Position([0, 2]),
    ]
    snake.shrink()
    assert list(snake.body) == [
        Position([3, 2]),
        Position([2, 2]),
        Position([1, 2]),
    ]
