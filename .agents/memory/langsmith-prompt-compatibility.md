---
name: LangSmith prompt compatibility
description: Compatibility between LangSmith chat prompt templates and agent APIs that accept plain system prompt text.
---

LangSmith's pulled chat prompts can be `ChatPromptTemplate` objects containing separate system and human message templates, while some agent constructors accept only a plain system-prompt string.

**Why:** Passing the template object directly can produce validation errors when the agent wraps it in a system message.

**How to apply:** Extract the system-message template text when handing a pulled prompt to an API that documents `system_prompt` as a string; keep the human-message template for the agent's runtime user input.