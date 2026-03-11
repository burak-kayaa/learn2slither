"""AppleManager class for managing apple spawning in the Snake game."""

Position = tuple[int, int]


class AppleManager:
    GREEN_COUNT = 2

    @staticmethod
    def spawn_initial(board, snake) -> tuple[set[Position], Position]:
        green_apples: set[Position] = set()
        occupied = set(snake.as_list())
        for _ in range(AppleManager.GREEN_COUNT):
            pos = board.random_empty_cell(occupied)
            green_apples.add(pos)
            occupied.add(pos)
        red_apple = board.random_empty_cell(occupied)
        return green_apples, red_apple

    @staticmethod
    def spawn_green(
        board, snake, green_apples: set[Position], red_apple: Position | None
    ) -> Position:
        occupied = set(snake.as_list()) | set(green_apples)
        if red_apple is not None:
            occupied.add(red_apple)
        return board.random_empty_cell(occupied)

    @staticmethod
    def spawn_red(board, snake, green_apples: set[Position]) -> Position:
        occupied = set(snake.as_list()) | set(green_apples)
        return board.random_empty_cell(occupied)
