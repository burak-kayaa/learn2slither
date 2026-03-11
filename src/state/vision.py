

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
        """Returns (object, distance_bucket) for the first object in each direction.

        The snake can see all cells along each axis (ray-casting). Reports the
        first non-empty cell encountered, or WALL when the board edge is reached.
        Distance is bucketed as: CLOSE (1), NEAR (2-3), FAR (4+).
        """
        head = game.snake.head
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        vision = {}
        snake_set = set(game.snake.as_list())
        for dir in directions:
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
    def print_vision(vision: dict[str, tuple[str, str]]) -> None:
        def symbol(cell: tuple[str, str]) -> str:
            obj_sym = {"WALL": "W", "SNAKE": "S", "GREEN_APPLE": "G", "RED_APPLE": "R"}.get(cell[0], "0")
            return f"{obj_sym}{cell[1][0]}"  # e.g. "WC" for WALL/CLOSE
        print(f"   {symbol(vision['UP'])}")
        print(f"{symbol(vision['LEFT'])}  H  {symbol(vision['RIGHT'])}")
        print(f"   {symbol(vision['DOWN'])}")