from langgraph.graph import StateGraph
from typing import Optional, TypedDict, List

from utils import clean_url

# State definition
class State(TypedDict):
    sample_website: str
    tech_stack: List[str]

# Node functions
def clean_sample_website(state: State):
    state["sample_website"] = clean_url(state["sample_website"])
    return state 