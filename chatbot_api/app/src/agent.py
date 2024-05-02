import os
from typing import Tuple, List

import dotenv
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_messages
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools.render import render_text_description_and_args
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.chat_tools import tools

dotenv.load_dotenv()

MODEL = os.getenv("MODEL")
OLLAMA_URL = os.getenv("OLLAMA_URL")

llm = ChatOllama(model=MODEL, timeout=120.0, base_url=OLLAMA_URL, num_gpu=1)

rendered_tools = (
    render_text_description_and_args(tools).replace("{", "{{").replace("}", "}}")
)
tool_names = [t.name for t in tools]

system_prompt = f"""Respond to the human as helpfully and accurately as possible. You have access to the following tools:

{rendered_tools}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tool_names}

Provide only ONE action per $JSON_BLOB, as shown:

```
{{{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}}}
```

Follow this format:

Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}}}

Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt,
        ),
        MessagesPlaceholder("chat_history", optional=True),
        (
            "human",
            """{input}

        {agent_scratchpad}
         (respond in a JSON blob no matter what)""",
        ),
    ]
)


def _format_chat_history(chat_history: List[Tuple[str, str]]):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer


chat_model_with_stop = llm.bind(stop=["\nObservation"])

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_messages(x["intermediate_steps"]),
        "chat_history": lambda x: (
            _format_chat_history(x["chat_history"]) if x.get("chat_history") else []
        ),
    }
    | prompt
    | chat_model_with_stop
    | JSONAgentOutputParser()
)


# Add typing for input
class AgentInput(BaseModel):
    input: str
    chat_history: List[Tuple[str, str]] = Field(
        ..., extra={"widget": {"type": "chat", "input": "input", "output": "output"}}
    )


executor = AgentExecutor(
    agent=agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
    handle_parsing_errors=True,
).with_types(input_type=AgentInput)
