import os
from operator import itemgetter

import dotenv
from langchain.tools.render import render_text_description
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from src.chain_tools import tools

dotenv.load_dotenv()


def tool_chain(model_output):
    """
    Executes a tool based on the output of a model.

    Parameters:
    model_output (dict): The output of a model, containing the name of the tool to execute and its arguments.

    Returns:
    The result of executing the tool.
    """
    tool_map = {t.name: t for t in tools}
    chosen_tool = tool_map[model_output["name"]]
    return itemgetter("arguments") | chosen_tool


MODEL = os.getenv("MODEL")
OLLAMA_URL = os.getenv("OLLAMA_URL")

llm = ChatOllama(model=MODEL, timeout=120.0, base_url=OLLAMA_URL, num_gpu=1)

rendered_tools = render_text_description(tools)

system_prompt = """[INST] <<SYS>>You are an assistant that has access to the following set of tools. Here are the names and descriptions for each tool:

<tools>
{tools}
</tools>

If you don't know the answer, just say that you don't know. Given the user input, return the name and input of the tool to use. Return your response as a JSON blob with 'name' and 'arguments' keys. Format the inputs properly as described by the tool.

<</SYS>>

 {question} [/INST]"""


prompt = ChatPromptTemplate.from_template(system_prompt)

chain = (
    prompt | llm | JsonOutputParser() | RunnablePassthrough.assign(output=tool_chain)
)


async def run_chain(input_text):
    """
    Runs the chain on the given input text asynchronously.

    Parameters:
    input_text (str): The input text to process.

    Returns:
    The result of running the chain on the input text.
    """
    return await chain.ainvoke({"tools": rendered_tools, "question": input_text})
