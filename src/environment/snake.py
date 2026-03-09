from collections import deque

Position = tuple[int, int]


class Snake:
    def __init__(self, initial_body: list[Position]):
        if not initial_body:
            raise ValueError("Initial body cannot be empty")
        self.body = deque(initial_body)

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
        self.body.appendleft(new_head)
        if not grow:
            self.body.pop()

    def shrink(self, amount: int = 1) -> None:
        for _ in range(amount):
            if self.body:
                self.body.pop()

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