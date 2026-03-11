def log_step(vision: dict[str, list[str]], action: str) -> None:
    print("Current vision:")
    for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
        print(f"  {direction}: {vision[direction]}")
    print(f"Chosen action: {action}")