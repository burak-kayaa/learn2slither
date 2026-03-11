from collections import deque

from src.config import Direction

Position = tuple[int, int]


class Snake:
    def __init__(self, initial_body: list[Position]):
        if not initial_body:
            raise ValueError("Initial body cannot be empty")
        self.body = deque(initial_body)
        self.direction = self._infer_initial_direction()

    @property
    def head(self) -> Position:
        return self.body[0]

    @property
    def tail(self) -> Position:
        return self.body[-1]

    def as_list(self) -> list[Position]:
        return list(self.body)

    def __len__(self) -> int:
        return len(self.body)

    def occupies(self, pos: Position) -> bool:
        return pos in self.body

    def move(self, new_head: Position, grow: bool = False) -> None:
        """Move the snake to a new head position. If grow is True, the snake will grow by one segment.
        """
        self.direction = self._direction_from_move(new_head)
        self.body.appendleft(new_head)
        if not grow:
            self.body.pop()

    def _direction_from_move(self, new_head: Position) -> str:
        hx, hy = self.head
        nx, ny = new_head
        dx, dy = nx - hx, ny - hy
        if dx == 1:
            return Direction.RIGHT
        if dx == -1:
            return Direction.LEFT
        if dy == 1:
            return Direction.DOWN
        return Direction.UP

    def shrink(self, amount: int = 1) -> None:
        for _ in range(amount):
            if self.body:
                self.body.pop()


    def _infer_initial_direction(self) -> str:
        if len(self.body) < 2:
            return Direction.RIGHT
        head_x, head_y = self.body[0]
        neck_x, neck_y = self.body[1]
        if head_x == neck_x:
            return Direction.DOWN if head_y > neck_y else Direction.UP
        else:
            return Direction.RIGHT if head_x > neck_x else Direction.LEFT

    @classmethod
    def create_default(cls, board_width: int = 10, board_height: int = 10) -> "Snake":
        head_x = board_width // 2
        head_y = board_height // 2

        initial_body = [
            (head_x, head_y),
            (head_x - 1, head_y),
            (head_x - 2, head_y),
        ]
        return cls(initial_body)