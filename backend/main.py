from langgraph.graph import StateGraph
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
def error_function(state: State):
    print(state["error_message"])
    return state

def clean_sample_website(state: State):
    if validators.url(state["sample_website"]):
        result = clean_url(state["sample_website"])
    else:
        state["error_message"] = "The given URL is invalid."
    
    if int(requests.get(result).status_code) / 100 == 2:
        state["sample_website"] = result
    else:
        state["error_message"] = "The given URL is invalid."

    return state