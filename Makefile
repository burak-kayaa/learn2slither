all:
	@uv run -m src.main --sessions 10000 --save trained_agent.json

load:
	@uv run -m src.main --load ./models/q_learning_agent_10000.json --dontlearn

t:
	@uv run pytest