from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.query import QueryInput, ChainQueryOutput, QueryOutput
from src.agent import executor
from src.chain import run_chain
from utils.async_utils import async_retry

app = FastAPI(
    title="Chatbot",
    description="Endpoints for a chatbot",
)

origins = [
    "http://localhost",
    "http://localhost:8501",
    "http://host.docker.internal:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@async_retry(max_retries=10, delay=1)
async def invoke_chain_with_retry(query: str):
    """Retry the agent if a tool fails to run.

    This can help when there are intermittent connection issues
    to external APIs.
    """
    return await run_chain(query)


@async_retry(max_retries=10, delay=1)
async def invoke_chat_with_retry(query: str):
    """Retry the agent if a tool fails to run.

    This can help when there are intermittent connection issues
    to external APIs.
    """
    return await executor.ainvoke({"input": query, "chat_history": []})


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/chain")
async def query_chain(query: QueryInput) -> ChainQueryOutput:
    query_response = await invoke_chain_with_retry(query.text)
    try:
        query_response["intermediate_steps"] = [
            str(s) for s in query_response["intermediate_steps"]
        ]
    except KeyError:
        query_response["intermediate_steps"] = []

    return query_response


@app.post("/chat")
async def query_chat(query: QueryInput) -> QueryOutput:
    query_response = await invoke_chat_with_retry(query.text)
    try:
        query_response["intermediate_steps"] = [
            str(s) for s in query_response["intermediate_steps"]
        ]
    except KeyError:
        query_response["intermediate_steps"] = []

    return query_response
