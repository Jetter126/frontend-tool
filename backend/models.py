from pydantic import BaseModel
from typing import Optional, List

# State definition
class State(BaseModel):
    sample_website: str
    tech_stack: List[str] = []
    error_message: Optional[str] = None