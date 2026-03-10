all:
	@uv run -m src.main

t:
	@uv run pytest