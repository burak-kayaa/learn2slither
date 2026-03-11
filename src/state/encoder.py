from src.config import RELATIVE_MAP


class StateEncoder:
    @staticmethod
    def encode(
        vision: dict[str, tuple[str, str]], current_direction: str
    ) -> tuple:
        """Encodes vision into a rotation-invariant state tuple.

        Each direction contributes (object, distance_bucket),
        giving a 6-element tuple:
        (ahead_obj, ahead_dist, left_obj, left_dist, right_obj, right_dist).
        """
        ahead, rel_left, rel_right = RELATIVE_MAP[current_direction]
        return (
            vision[ahead][0],   vision[ahead][1],
            vision[rel_left][0],  vision[rel_left][1],
            vision[rel_right][0], vision[rel_right][1],
        )
