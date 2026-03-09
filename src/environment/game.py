from dataclasses import dataclass

from src.environment.board import Board
from src.environment.snake import Snake
from src.environment.apples import AppleManager

Position = tuple[int, int]

DIRECTION_DELTAS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}


@dataclass
class StepResult:
    event: str
    done: bool
    score_delta: int = 0


class Game:
    def __init__(self, width: int = 10, height: int = 10):
        self.board = Board(width, height)
        self.snake = Snake.create_default(width, height)
        self.green_apples, self.red_apple = AppleManager.spawn_initial(
            self.board,
            self.snake,
        )
        self.done = False

    def reset(self) -> None:
        self.snake = Snake.create_default(self.board.width, self.board.height)
        self.green_apples, self.red_apple = AppleManager.spawn_initial(
            self.board,
            self.snake,
        )
        self.done = False

    def get_next_head(self, action: str) -> Position:
        if action not in DIRECTION_DELTAS:
            raise ValueError(f"Invalid action: {action}")

        dx, dy = DIRECTION_DELTAS[action]
        x, y = self.snake.head
        return (x + dx, y + dy)

    def will_hit_self(self, next_head: Position, grow: bool) -> bool:
        body_positions = self.snake.as_list()
        if grow:
            return next_head in body_positions
        return next_head in body_positions[:-1]

    def step(self, action: str) -> StepResult:
        if self.done:
            return StepResult(event="GAME_ALREADY_OVER", done=True, score_delta=0)
        next_head = self.get_next_head(action)
        if not self.board.is_inside(next_head):
            self.done = True
            return StepResult(event="WALL_COLLISION", done=True, score_delta=0)
        is_green = next_head in self.green_apples
        is_red = next_head == self.red_apple
        grow = is_green
        if self.will_hit_self(next_head, grow=grow):
            self.done = True
            return StepResult(event="SELF_COLLISION", done=True, score_delta=0)
        self.snake.move(next_head, grow=grow)
        if is_green:
            self.green_apples.remove(next_head)
            new_green = AppleManager.spawn_green(
                self.board,
                self.snake,
                self.green_apples,
                self.red_apple,
            )
            self.green_apples.add(new_green)
            return StepResult(event="GREEN_APPLE", done=False, score_delta=1)
        if is_red:
            self.snake.shrink(1)
            if len(self.snake) == 0:
                self.done = True
                return StepResult(event="ZERO_LENGTH", done=True, score_delta=-1)
            self.red_apple = AppleManager.spawn_red(
                self.board,
                self.snake,
                self.green_apples,
            )
            return StepResult(event="RED_APPLE", done=False, score_delta=-1)
        return StepResult(event="MOVE", done=False, score_delta=0)

    def get_state_snapshot(self) -> dict:
        return {
            "snake": self.snake.as_list(),
            "head": self.snake.head,
            "green_apples": list(self.green_apples),
            "red_apple": self.red_apple,
            "done": self.done,
        }

    def print_board(self) -> None:
        grid = [["." for _ in range(self.board.width)] for _ in range(self.board.height)]
        for x, y in self.green_apples:
            grid[y][x] = "G"
        if self.red_apple is not None:
            rx, ry = self.red_apple
            grid[ry][rx] = "R"
        snake_positions = self.snake.as_list()
        for i, (x, y) in enumerate(snake_positions):
            grid[y][x] = "H" if i == 0 else "S"
        for row in grid:
            print(" ".join(row))
        print()