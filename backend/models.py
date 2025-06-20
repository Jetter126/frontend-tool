from typing import Optional, List

from pydantic import BaseModel


class State(BaseModel):
    """State definition for the agent workflow"""
    sample_website: str
    tech_stack: List[str] = []
    error_message: Optional[str] = None