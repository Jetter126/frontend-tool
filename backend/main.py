from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
import validators
import requests

from models import State
from utils import clean_url


# Initialise LLM
load_dotenv()
llm = init_chat_model(os.getenv("MODEL_NAME"))


# Node functions
def error_function(state: State) -> State:
    print(state.error_message)
    return state


def clean_sample_website(state: State) -> State:
    result = clean_url(state.sample_website)
    if validators.url(result) and int(requests.get(result).status_code / 100) == 2:
        state.sample_website = result
    else:
        state.error_message = "The given URL is invalid."

    return state


# Building the graph
graph_builder = StateGraph(State)

graph_builder.add_node("clean_sample_website", clean_sample_website)

graph_builder.add_edge(START, "clean_sample_website")
graph_builder.add_edge("clean_sample_website", END)

graph = graph_builder.compile()

initial_state = State(sample_website="https://www.github.com/homepage?view=123/123")
result = graph.invoke(initial_state)
print(result["sample_website"])