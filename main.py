import anthropic
import os
from pathlib import Path
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent
from langsmith import Client
import datetime


open_router_api = os.getenv("OPENROUTER_API_KEY")
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
anthropic_api = os.getenv("ANTHROPIC_API_KEY")



# Prompts

client = Client()
pulled_prompt = client.pull_prompt("orchestrator:production")
prompt_pull = pulled_prompt.invoke({"date": datetime.date.today()})
messages = prompt_pull.to_messages()
first = messages[0]
orchestrator_prompt = first.content
print(orchestrator_prompt)


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.3-flash",
    tools=[internet_search],
    system_prompt=orchestrator_prompt,
)

stock = "BOA"


result = agent.invoke(
    {"messages": [{"role": "user", "content": f"Please analyze the stock {stock}."}]}
)

# Print the agent's response
content = result["messages"][-1].content
if isinstance(content, list):
    print("".join(block["text"] for block in content if block.get("type") == "text"))
else:
    print(content)
