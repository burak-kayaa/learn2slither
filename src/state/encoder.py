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
    def encode(vision: dict[str, tuple[str, str]], current_direction: str) -> tuple:
        """Encodes vision into a rotation-invariant state tuple.

        Each direction contributes (object, distance_bucket), giving a 6-element
        tuple: (ahead_obj, ahead_dist, left_obj, left_dist, right_obj, right_dist).
        """
        ahead, rel_left, rel_right = _RELATIVE_MAP[current_direction]
        return (
            vision[ahead][0],   vision[ahead][1],
            vision[rel_left][0],  vision[rel_left][1],
            vision[rel_right][0], vision[rel_right][1],
        )