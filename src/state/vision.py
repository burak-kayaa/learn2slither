from src.config import ACTIONS, CellType
from src.environment.game import DIRECTION_DELTAS, Game


def _bucket_distance(dist: int) -> str:
    """Bucket a raw cell distance into a categorical label."""
    if dist <= 1:
        return "CLOSE"
    if dist <= 3:
        return "NEAR"
    return "FAR"


class VisionInterpreter:
    @staticmethod
    def extract(game: Game) -> dict[str, tuple[str, str]]:
        """Returns (object, distance_bucket) for the first object
        in each direction.

        The snake can see all cells along each axis (ray-casting).
        Reports the first non-empty cell encountered, or WALL when
        the board edge is reached.
        Distance is bucketed as: CLOSE (1), NEAR (2-3), FAR (4+).
        """
        head = game.snake.head
        vision = {}
        snake_set = set(game.snake.as_list())
        for dir in ACTIONS:
            dx, dy = DIRECTION_DELTAS[dir]
            x, y = head
            dist = 0
            while True:
                x += dx
                y += dy
                dist += 1
                pos = (x, y)
                if not game.board.is_inside(pos):
                    vision[dir] = ("WALL", _bucket_distance(dist))
                    break
                elif pos in snake_set:
                    vision[dir] = ("SNAKE", _bucket_distance(dist))
                    break
                elif pos in game.green_apples:
                    vision[dir] = ("GREEN_APPLE", _bucket_distance(dist))
                    break
                elif pos == game.red_apple:
                    vision[dir] = ("RED_APPLE", _bucket_distance(dist))
                    break
        return vision

    @staticmethod
    def print_cross(game: Game, action: str) -> None:
        """Print the agent's full directional vision as a cross to stdout.

        Shows every cell seen along each axis from the snake's head,
        using: H=head, 0=empty, W=wall, S=snake, G=green apple, R=red apple.
        """
        head = game.snake.head
        snake_set = set(game.snake.as_list())

        def cell_char(pos: tuple) -> str:
            if not game.board.is_inside(pos):
                return CellType.WALL
            if pos in snake_set:
                return CellType.SNAKE
            if pos in game.green_apples:
                return CellType.GREEN_APPLE
            if pos == game.red_apple:
                return CellType.RED_APPLE
            return CellType.EMPTY

        def ray(direction: str) -> list[str]:
            dx, dy = DIRECTION_DELTAS[direction]
            x, y = head
            cells = []
            while True:
                x += dx
                y += dy
                pos = (x, y)
                cells.append(cell_char(pos))
                if not game.board.is_inside(pos):
                    break
            return cells
        up_ray = ray("UP")[::-1]
        down_ray = ray("DOWN")
        left_ray = ray("LEFT")[::-1]
        right_ray = ray("RIGHT")
        indent = " " * len(left_ray)
        h_line = "".join(left_ray) + "H" + "".join(right_ray)
        print(f"Action: {action}")
        for ch in up_ray:
            print(f"{indent}{ch}")
        print(h_line)
        for ch in down_ray:
            print(f"{indent}{ch}")
        print()
