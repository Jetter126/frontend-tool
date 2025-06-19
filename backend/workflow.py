import os
import requests
from typing import Any, Dict

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
import validators

from models import State
from utils import clean_url


class Workflow:
    def __init__(self):
        self.llm = init_chat_model(os.getenv("MODEL_NAME"))
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph_builder = StateGraph(State)

        graph_builder.add_node("clean_sample_website", self._clean_sample_website)

        graph_builder.add_edge(START, "clean_sample_website")
        graph_builder.add_edge("clean_sample_website", END)

        return graph_builder.compile()

    def _clean_sample_website(self, state: State) -> Dict[str, Any]:
        result = clean_url(state.sample_website)
        if validators.url(result) and int(requests.get(result).status_code / 100) == 2:
            state.sample_website = result
        else:
            state.error_message = "The given URL is invalid."

        return state

    def run(self):
        initial_state = State(sample_website="https://www.github.com/homepage?view=123/123")
        final_state = self.workflow.invoke(initial_state)
        return State(**final_state)
    
"""
def error_function(state: State) -> State:
    print(state.error_message)
    return state
"""