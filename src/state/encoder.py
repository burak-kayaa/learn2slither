from src.config import Direction

class StateEncoder:

    @staticmethod
    def encode(vision: dict[Direction, list[str]]) -> tuple:
        """
        Encodes the vision into a tuple of strings.
        """
        return (
            tuple(vision[Direction.UP]),
            tuple(vision[Direction.DOWN]),
            tuple(vision[Direction.LEFT]),
            tuple(vision[Direction.RIGHT]),
        )