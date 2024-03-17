from pydantic import BaseModel, Field

class ServerEvents(BaseModel):
    PROMPT_MESSAGE: str = Field('prompt_message', const=True)
    GRAVITY: float = Field(9.81, const=True)