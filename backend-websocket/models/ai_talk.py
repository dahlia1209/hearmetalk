from pydantic import BaseModel, Field
from typing import Literal

class ServerEvents:
    PROMPT_MESSAGE = 'prompt_message'

class ClientEvents:
    RECEIVE_PROMPT_MESSAGE='receive_prompt_message'