from typing import Annotated, TypedDict
from pydantic import BaseModel
from langgraph.graph.message import add_messages


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


class State(TypedDict):
    messages: Annotated[list, add_messages]
    coin_name: str
