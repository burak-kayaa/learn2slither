import pytest

from src.environment.board import Board
from src.environment.game import Position


def test_position_inside_board() -> None:
    board = Board(width=10, height=10)
    assert board.is_inside(Position([0, 0])) is True
    assert board.is_inside(Position([9, 9])) is True


def test_position_outside_board() -> None:
    board = Board(width=10, height=10)
    assert board.is_inside(Position([-1, 0])) is False
    assert board.is_inside(Position([10, 5])) is False
    assert board.is_inside(Position([5, 10])) is False


def test_board_dimensions_must_be_positive() -> None:
    with pytest.raises(ValueError):
        Board(width=0, height=10)
    with pytest.raises(ValueError):
        Board(width=10, height=0)
    with pytest.raises(ValueError):
        Board(width=-1, height=10)
    with pytest.raises(ValueError):
        Board(width=10, height=-1)
        

def test_board_initialization() -> None:
    board = Board(width=5, height=5)
    assert board.width == 5
    assert board.height == 5
    assert board.is_inside(Position([2, 2])) is True
    assert board.is_inside(Position([5, 5])) is False