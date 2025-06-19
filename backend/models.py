from typing import TypedDict, List

# State definition
class State(TypedDict):
    sample_website: str
    tech_stack: List[str]
    error_message: str