import json
import os
import requests
from typing import Any, Dict

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
import validators

from models import State
from utils import clean_url, extract_tech_stack


class Workflow:
    def __init__(self):
        self.llm = init_chat_model(os.getenv("MODEL_NAME"))
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        """Builds the workflow graph using nodes and edges."""
        graph_builder = StateGraph(State)

        graph_builder.add_node("clean_sample_website", self._clean_sample_website)
        graph_builder.add_node("extract_tech_stack", self._extract_tech_stack)

        graph_builder.add_edge(START, "clean_sample_website")
        graph_builder.add_edge("clean_sample_website", "extract_tech_stack")
        graph_builder.add_edge("extract_tech_stack", END)

        return graph_builder.compile()

    def _clean_sample_website(self, state: State) -> Dict[str, Any]:
        """Cleans and validates the sample website submitted by the user."""
        result = clean_url(state.sample_website)
        if validators.url(result) and int(requests.get(result).status_code / 100) == 2:
            return {"sample_website": result}
        else:
            return {"error_message": "The given URL is invalid."}
        
    def _extract_tech_stack(self, state: State) -> Dict[str, Any]:
        """Extracts the tech stack used to build the sample website."""
        with open("tech_stacks.json", "r") as file:
            data = json.load(file)

        try:
            tech_stack = data[state.sample_website]
        except:
            tech_stack = extract_tech_stack(state.sample_website)
            data[state.sample_website] = tech_stack
            with open("tech_stacks.json", "w") as file:
                json.dump(data, file)

        return {"tech_stack": tech_stack}

    def run(self, sample_website: str):
        """Takes in user input and runs the agent."""
        initial_state = State(sample_website=sample_website)
        final_state = self.workflow.invoke(initial_state)
        return State(**final_state)
    
"""
def error_function(state: State) -> State:
    print(state.error_message)
    return state
"""