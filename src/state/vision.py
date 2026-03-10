

from src.environment.game import DIRECTION_DELTAS, Game

class VisionInterpreter:
    @staticmethod
    def extract(game: Game) -> dict[str, list[str]]:
        head = game.snake.head
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        vision = {dir: [] for dir in directions}
        for dir in directions:
            dx, dy = DIRECTION_DELTAS[dir]
            x, y = head
            while True:
                x += dx
                y += dy
                pos = (x, y)

                if not game.board.is_inside(pos):
                    vision[dir].append("WALL")
                    break
                elif pos in game.snake.as_list():
                    vision[dir].append("SNAKE")
                elif pos in game.green_apples:
                    vision[dir].append("GREEN_APPLE")
                elif pos == game.red_apple:
                    vision[dir].append("RED_APPLE")
                else:
                    vision[dir].append("EMPTY")
        return vision

    @staticmethod
    def print_vision(vision: dict[str, list[str]]) -> None:
        def symbol(cell: str) -> str:
            if cell == "WALL":
                return "W"
            elif cell == "SNAKE":
                return "S"
            elif cell == "GREEN_APPLE":
                return "G"
            elif cell == "RED_APPLE":
                return "R"
            else:
                return "0"
        up = [symbol(c) for c in reversed(vision["UP"])]
        down = [symbol(c) for c in vision["DOWN"]]
        left = [symbol(c) for c in reversed(vision["LEFT"])]
        right = [symbol(c) for c in vision["RIGHT"]]
        padding = " " * (len(left))
        for cell in up:
            print(f"{padding}{cell}")
        middle_row = left + ["H"] + right
        print("".join(middle_row))
        for cell in down:
            print(f"{padding}{cell}")