from langgraph.graph import StateGraph, START, END
from typing import Optional, TypedDict, List
import validators
import requests

from utils import clean_url

# State definition
class State(TypedDict):
    sample_website: str
    tech_stack: List[str]
    error_message: str

# Node functions
def error_function(state: State) -> State:
    print(state["error_message"])
    return state

def clean_sample_website(state: State) -> State:
    result = clean_url(state["sample_website"])
    if validators.url(result) and int(requests.get(result).status_code) / 100 == 2:
        state["sample_website"] = result
    else:
        state["error_message"] = "The given URL is invalid."

    return state

# Building the graph
graph_builder = StateGraph(State)

graph_builder.add_node("clean_sample_website", clean_sample_website)

graph_builder.add_edge(START, "clean_sample_website")
graph_builder.add_edge("clean_sample_website", END)

graph = graph_builder.compile()

result = graph.invoke({"sample_website": "https://www.github.com/homepage?view=123/123"})
print(result["sample_website"])