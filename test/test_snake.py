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
    body = list(snake.body)
    assert len(body) == 3

    head_x, head_y = body[0]
    neck_x, neck_y = body[1]
    tail_x, tail_y = body[2]

    assert 0 <= head_x < 10
    assert 0 <= head_y < 10
    assert (neck_x, neck_y) == (head_x - 1, head_y)
    assert (tail_x, tail_y) == (head_x - 2, head_y)
    assert 2 <= head_x <= 9


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
