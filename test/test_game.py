import pytest

# Position = tuple[int, int]

# DIRECTION_DELTAS = {
#     "UP": (0, -1),
#     "DOWN": (0, 1),
#     "LEFT": (-1, 0),
#     "RIGHT": (1, 0),
# }


# @dataclass
# class StepResult:
#     event: str
#     done: bool
#     score_delta: int = 0


# class Game:
#     def __init__(self, width: int = 10, height: int = 10):
#         self.board = Board(width, height)
#         self.snake = Snake.create_default(width, height)
#         self.green_apples, self.red_apple = AppleManager.spawn_initial(
#             self.board,
#             self.snake,
#         )
#         self.done = False

#     def reset(self) -> None:
#         self.snake = Snake.create_default(self.board.width, self.board.height)
#         self.green_apples, self.red_apple = AppleManager.spawn_initial(
#             self.board,
#             self.snake,
#         )
#         self.done = False

#     def get_next_head(self, action: str) -> Position:
#         if action not in DIRECTION_DELTAS:
#             raise ValueError(f"Invalid action: {action}")

#         dx, dy = DIRECTION_DELTAS[action]
#         x, y = self.snake.head
#         return (x + dx, y + dy)

#     def will_hit_self(self, next_head: Position, grow: bool) -> bool:
#         body_positions = self.snake.as_list()
#         if grow:
#             return next_head in body_positions
#         return next_head in body_positions[:-1]

#     def step(self, action: str) -> StepResult:
#         if self.done:
#             return StepResult(event="GAME_ALREADY_OVER", done=True, score_delta=0)
#         next_head = self.get_next_head(action)
#         if not self.board.is_inside(next_head):
#             self.done = True
#             return StepResult(event="WALL_COLLISION", done=True, score_delta=0)
#         is_green = next_head in self.green_apples
#         is_red = next_head == self.red_apple
#         grow = is_green
#         if self.will_hit_self(next_head, grow=grow):
#             self.done = True
#             return StepResult(event="SELF_COLLISION", done=True, score_delta=0)
#         self.snake.move(next_head, grow=grow)
#         if is_green:
#             self.green_apples.remove(next_head)
#             new_green = AppleManager.spawn_green(
#                 self.board,
#                 self.snake,
#                 self.green_apples,
#                 self.red_apple,
#             )
#             self.green_apples.add(new_green)
#             return StepResult(event="GREEN_APPLE", done=False, score_delta=1)
#         if is_red:
#             self.snake.shrink(1)
#             if len(self.snake) == 0:
#                 self.done = True
#                 return StepResult(event="ZERO_LENGTH", done=True, score_delta=-1)
#             self.red_apple = AppleManager.spawn_red(
#                 self.board,
#                 self.snake,
#                 self.green_apples,
#             )
#             return StepResult(event="RED_APPLE", done=False, score_delta=-1)
#         return StepResult(event="MOVE", done=False, score_delta=0)

#     def get_state_snapshot(self) -> dict:
#         return {
#             "snake": self.snake.as_list(),
#             "head": self.snake.head,
#             "green_apples": list(self.green_apples),
#             "red_apple": self.red_apple,
#             "done": self.done,
#         }

#     def print_board(self) -> None:
#         grid = [["." for _ in range(self.board.width)] for _ in range(self.board.height)]
#         for x, y in self.green_apples:
#             grid[y][x] = "G"
#         if self.red_apple is not None:
#             rx, ry = self.red_apple
#             grid[ry][rx] = "R"
#         snake_positions = self.snake.as_list()
#         for i, (x, y) in enumerate(snake_positions):
#             grid[y][x] = "H" if i == 0 else "S"
#         for row in grid:
#             print(" ".join(row))
#         print()
from src.environment.game import Game
from src.environment.board import Board
from src.environment.snake import Snake
from src.environment.apples import AppleManager

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
    assert result.event == "WALL_COLLISION"
    assert result.done
    assert game.done
    
    
def test_game_step_self_collision():
    game = Game(width=5, height=5)
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
    assert result.event == "SELF_COLLISION"
    assert result.done
    assert game.done
    
    
    
def test_game_step_green_apple():
    game = Game(width=5, height=5)
    # Place a green apple directly in front of the snake
    head_x, head_y = game.snake.head
    green_apple_pos = (head_x, head_y - 1)
    game.green_apples.add(green_apple_pos)
    result = game.step("UP")
    assert result.event == "GREEN_APPLE"
    assert not result.done
    assert result.score_delta == 1
    assert len(game.snake.body) == 4  # Snake should grow by 1
    
    
def test_game_step_red_apple():
    game = Game(width=5, height=5)
    head_x, head_y = game.snake.head
    red_apple_pos = (head_x, head_y - 1)
    game.red_apple = red_apple_pos
    result = game.step("UP")
    assert result.event == "RED_APPLE"
    assert not result.done
    assert result.score_delta == -1
    assert len(game.snake.body) == 2
    
    
def test_game_step_zero_length():
    game = Game(width=8, height=8)
    # place red apple 3 times in front of the snake to shrink it to zero
    head_x, head_y = game.snake.head
    # print board
    for _ in range(3):
        head_x, head_y = game.snake.head
        red_apple_pos = (head_x, head_y - 1)
        game.red_apple = red_apple_pos
        result = game.step("UP")
    assert result.event == "ZERO_LENGTH"
    assert result.done    
    
def test_game_step_after_game_over():
    game = Game(width=5, height=5)
    for _ in range(3):
        game.step("UP")
    assert game.done
    
    result = game.step("UP")
    assert result.event == "GAME_ALREADY_OVER"
    assert result.done
    assert result.score_delta == 0