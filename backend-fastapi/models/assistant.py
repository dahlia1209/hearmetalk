from pydantic import BaseModel, Field, validator
from typing import List, Optional,Literal
from uuid import uuid4

class Tool(BaseModel):
    type: str

class AssistantsCreate(BaseModel):
    name: str = Field(default_factory=lambda: str(uuid4()))
    instructions: str=None
    tools: List[Tool]=None
    model: Literal["gpt-4", "gpt-4-turbo-preview", "gpt-3.5-turbo"]="gpt-4"

class Message(BaseModel):
    role: str
    content: str