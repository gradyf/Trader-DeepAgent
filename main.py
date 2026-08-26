import os
from pathlib import Path
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

or_api = os.getenv("OPENROUTER_API_KEY")
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def get_weather(city: str) -> str:
    """Get weather for a given city. Only return the weather, nothing else."""
    return f"It's always sunny in {city}!"


# System prompt to steer the agent to be an expert researcher
orchestrator_prompt = Path("prompts/orchestrator.md").read_text(encoding="utf-8")

print(orchestrator_prompt)


agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.3-flash",
    tools=[get_weather],
    system_prompt=orchestrator_prompt,
)


result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in Denver today?"}]}
)

# Print the agent's response
content = result["messages"][-1].content
if isinstance(content, list):
    print("".join(block["text"] for block in content if block.get("type") == "text"))
else:
    print(content)
