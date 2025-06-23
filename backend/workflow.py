import json
import os
import requests
from typing import Any, Dict

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
import validators

from models import State
from prompts import FrontendDevelopmentPrompts
from utils import clean_url, extract_tech_stack, parse_generated_code, write_generated_code


class Workflow:
    def __init__(self):
        self.llm = init_chat_model(os.getenv("MODEL_NAME"))
        self.prompts = FrontendDevelopmentPrompts()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        """Builds the workflow graph using nodes and edges."""
        graph_builder = StateGraph(State)

        graph_builder.add_node("clean_sample_website", self._clean_sample_website)
        graph_builder.add_node("extract_tech_stack", self._extract_tech_stack)
        graph_builder.add_node("generate_frontend", self._generate_frontend)

        graph_builder.add_edge(START, "clean_sample_website")
        graph_builder.add_edge("clean_sample_website", "extract_tech_stack")
        graph_builder.add_edge("extract_tech_stack", "generate_frontend")
        graph_builder.add_edge("generate_frontend", END)

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
        print(f"🔍 Examining {state.sample_website}")

        with open("tech_stacks.json", "r") as file:
            data = json.load(file)

        try:
            tech_stack = data[state.sample_website]
        except:
            tech_stack = extract_tech_stack(state.sample_website)
            data[state.sample_website] = tech_stack
            with open("tech_stacks.json", "w") as file:
                json.dump(data, file)

        if (len(tech_stack) > 0):
            print(f"✅ Done! Here's the tech stack: {', '.join(tech_stack)}")
        else:
            print(f"❌ Couldn't find the tech stack :/")

        return {"tech_stack": tech_stack}

    def _generate_frontend(self, state: State) -> Dict[str, Any]:
        """Generates code to produce a frontend similar to the sample website using the extracted tech stack."""
        print("Generating the frontend...")

        messages = [
            SystemMessage(content=self.prompts.CODE_GENERATION_SYSTEM),
            HumanMessage(content=self.prompts.code_generation_user(state.sample_website, state.tech_stack))
        ]

        try:
            response = self.llm.invoke(messages)
            generated_frontend = parse_generated_code(response.content)

            current_dir = os.path.dirname(__file__)
            base_output_dir = os.path.join(current_dir, "..", "output")
            base_output_dir = os.path.abspath(base_output_dir)

            for filename, content in generated_frontend.items():
                write_generated_code(current_dir, base_output_dir, filename, content)

            print(f"✅ Created the following files: {', '.join(generated_frontend.keys())}")
            return {"generated_frontend": generated_frontend}
        except Exception as e:
            print(e)
            return {"generated_frontend": {}}

    def run(self, sample_website: str):
        """Takes in user input and runs the agent."""
        initial_state = State(sample_website=sample_website)
        final_state = self.workflow.invoke(initial_state)
        return State(**final_state)