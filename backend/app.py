from fastapi import HTTPException
from models import ChatRequest, ChatResponse, State
from langgraph.graph import StateGraph, MessagesState
# from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from config import chat_gpt
import requests
import re
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import load_env_variables

# Load environment variables
load_env_variables()

# Set up the FastAPI app and cors middleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the state graph
graph_builder = StateGraph(MessagesState)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        state: State = {
            "messages": [HumanMessage(content=request.prompt)],
            "coin_name": "",
        }
        final_state = app_runnable.invoke(
            state, config={"configurable": {"thread_id": 1}}
        )
        return ChatResponse(response=final_state["messages"][-1].content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def chatbot(state: MessagesState) -> MessagesState:
    user_message = state["messages"][-1].content.lower()
    coin_match = re.search(r"\b(price of|what is the price of) (\w+)\b", user_message)
    if coin_match:
        coin_name = coin_match.group(2).lower()
        state["coin_name"] = coin_name
        state["messages"].append(
            HumanMessage(content=f"Fetching the price of {coin_name}...")
        )
        state["_next_node"] = "query_coin_price"
        return state

    elif re.search(r"\bwhat stable coin\b", user_message):
        state["messages"].append(
            HumanMessage(content="Fetching the list of stablecoins...")
        )
        state["_next_node"] = "list_stablecoins"
        return state

    else:
        response_content = chat_gpt(user_message)
        state["messages"].append(HumanMessage(content=response_content))
        state["_next_node"] = None
        return state


def query_coin_price(state: State) -> State:
    coin_name = state.get("coin_name")
    if not coin_name:
        state["messages"].append(HumanMessage(content="Coin name not found."))
        state["_next_node"] = None
        return state

    url = f"https://coins.llama.fi/prices/current/coingecko:{coin_name}?searchWidth=4h"
    response = requests.get(url)
    if response.status_code == 200:
        price_data = response.json()
        print(response.status_code)
        print(response.json())
        price = (
            price_data.get("coins", {})
            .get(f"coingecko:{coin_name}", {})
            .get("price", "unknown")
        )
        message = f"The current price of {coin_name} is {price}."
    else:
        message = f"Failed to retrieve the price for {coin_name}."

    state["messages"].append(HumanMessage(content=message))
    state["_next_node"] = None
    return state


def list_stablecoins(state: MessagesState) -> MessagesState:
    print(state)
    url = "https://stablecoins.llama.fi/stablecoins?includePrices=true"
    response = requests.get(url)
    if response.status_code == 200:
        stablecoins_data = response.json()
        stablecoins_list = [
            coin["name"] for coin in stablecoins_data.get("peggedAssets", [])
        ]
        message = f"List of stablecoins: {', '.join(stablecoins_list)}"
    else:
        message = "Failed to retrieve the list of stablecoins."

    state["messages"].append(HumanMessage(content=message))
    state["_next_node"] = None
    return state


# Add nodes to the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("query_coin_price", query_coin_price)
graph_builder.add_node("list_stablecoins", list_stablecoins)

# Define the edge to transition from chatbot to query_coin_price
graph_builder.add_edge("chatbot", "query_coin_price")
graph_builder.add_edge("chatbot", "list_stablecoins")

# Set entry and finish points
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("query_coin_price")
graph_builder.set_finish_point("list_stablecoins")

# Initialize memory to persist state between graph runs
# checkpointer = MemorySaver()
# app_runnable = graph_builder.compile(checkpointer=checkpointer)

app_runnable = graph_builder.compile()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
