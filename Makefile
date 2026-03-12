all:
	@uv run -m src.main --sessions 10000 --save trained_agent.json

load:
	@uv run -m src.main --load ./models/q_learning_agent_10000.json --dont-learn --render

ui:
	@uv run -m src.main --ui

t:
	@uv run pytest