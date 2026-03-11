

from src.environment.game import DIRECTION_DELTAS, Game

class VisionInterpreter:
    @staticmethod
    def extract(game: Game) -> dict[str, str]:
        head = game.snake.head
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        vision = {}
        snake_set = set(game.snake.as_list())
        for dir in directions:
            dx, dy = DIRECTION_DELTAS[dir]
            x, y = head
            while True:
                x += dx
                y += dy
                pos = (x, y)
                if not game.board.is_inside(pos):
                    vision[dir] = "WALL"
                    break
                elif pos in snake_set:
                    vision[dir] = "SNAKE"
                    break
                elif pos in game.green_apples:
                    vision[dir] = "GREEN_APPLE"
                    break
                elif pos == game.red_apple:
                    vision[dir] = "RED_APPLE"
                    break
        return vision

    @staticmethod
    def print_vision(vision: dict[str, str]) -> None:
        def symbol(cell: str) -> str:
            return {"WALL": "W", "SNAKE": "S", "GREEN_APPLE": "G", "RED_APPLE": "R"}.get(cell, "0")
        print(f"  {symbol(vision['UP'])}")
        print(f"{symbol(vision['LEFT'])} H {symbol(vision['RIGHT'])}")
        print(f"  {symbol(vision['DOWN'])}")