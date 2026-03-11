from src.config import Direction

# (ahead, relative_left, relative_right) mapping per absolute heading
_RELATIVE_MAP: dict[str, tuple[str, str, str]] = {
    Direction.RIGHT: (Direction.RIGHT, Direction.UP,   Direction.DOWN),
    Direction.LEFT:  (Direction.LEFT,  Direction.DOWN,  Direction.UP),
    Direction.UP:    (Direction.UP,    Direction.LEFT,  Direction.RIGHT),
    Direction.DOWN:  (Direction.DOWN,  Direction.RIGHT, Direction.LEFT),
}


class StateEncoder:
    @staticmethod
    def encode(vision: dict[str, str], current_direction: str) -> tuple:
        """Encodes vision into a rotation-invariant (ahead, left, right) tuple."""
        ahead, rel_left, rel_right = _RELATIVE_MAP[current_direction]
        return (
            vision[ahead],
            vision[rel_left],
            vision[rel_right],
        )