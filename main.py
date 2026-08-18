from deepagents import create_deep_agent

# Anthropic's built-in web search — no extra install or API key needed
internet_search = {"type": "web_search_20260209", "name": "web_search"}


# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[internet_search],
    system_prompt=research_instructions,
)


result = agent.invoke({"messages": [{"role": "user", "content": "What is langgraph?"}]})

# Print the agent's response
content = result["messages"][-1].content
if isinstance(content, list):
    print("".join(block["text"] for block in content if block.get("type") == "text"))
else:
    print(content)
