from src.state.encoder import StateEncoder


def test_state_encoder_facing_right():
    # Facing RIGHT: ahead=RIGHT, rel_left=UP, rel_right=DOWN
    vision = {
        "UP": ("WALL", "CLOSE"),
        "DOWN": ("GREEN_APPLE", "NEAR"),
        "LEFT": ("SNAKE", "FAR"),
        "RIGHT": ("WALL", "FAR"),
    }
    # ahead=(WALL,FAR), rel_left=(WALL,CLOSE), rel_right=(GREEN_APPLE,NEAR)
    result = StateEncoder.encode(vision, "RIGHT")
    assert result == ("WALL", "FAR", "WALL", "CLOSE", "GREEN_APPLE", "NEAR")


def test_state_encoder_facing_up():
    # Facing UP: ahead=UP, rel_left=LEFT, rel_right=RIGHT
    vision = {
        "UP": ("GREEN_APPLE", "NEAR"),
        "DOWN": ("SNAKE", "CLOSE"),
        "LEFT": ("WALL", "CLOSE"),
        "RIGHT": ("WALL", "FAR"),
    }
    # ahead=(GREEN_APPLE,NEAR), rel_left=(WALL,CLOSE), rel_right=(WALL,FAR)
    result = StateEncoder.encode(vision, "UP")
    assert result == ("GREEN_APPLE", "NEAR", "WALL", "CLOSE", "WALL", "FAR")


def test_state_encoder_facing_down():
    # Facing DOWN: ahead=DOWN, rel_left=RIGHT, rel_right=LEFT
    vision = {
        "UP": ("WALL", "FAR"),
        "DOWN": ("GREEN_APPLE", "NEAR"),
        "LEFT": ("WALL", "CLOSE"),
        "RIGHT": ("SNAKE", "CLOSE"),
    }
    # ahead=(GREEN_APPLE,NEAR), rel_left=(SNAKE,CLOSE), rel_right=(WALL,CLOSE)
    result = StateEncoder.encode(vision, "DOWN")
    assert result == ("GREEN_APPLE", "NEAR", "SNAKE", "CLOSE", "WALL", "CLOSE")
