from typing import Literal,Optional,List
from pydantic import BaseModel

class Message(BaseModel):
    message_id: str = ""
    is_user: bool = True
    content: str = ""
    role: Literal["user", "assistant", "system"] = "user"

class MessageDto(BaseModel):
    role: Literal["user", "assistant", "system"] = "user"
    content: str = ""


class ChatCompletionSettings(BaseModel):
    model: Literal["gpt-3.5-turbo", "gpt-4-1106-preview", "gpt-4"] = "gpt-3.5-turbo"
    messages: List[MessageDto] = []
    temperature: float = 1.0
    max_tokens: int = 1024
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stream: bool=False

class MessageResponseDto(BaseModel):
    content: str = ""
    role: Literal["user", "assistant", "system"] = "user"
    function_call: Optional[str] = None
    tool_calls: Optional[str] = None

class Choice(BaseModel):
    finish_reason: Literal["stop", "length", "error"]
    index: int
    message: MessageResponseDto

class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    choices: List[Choice]
    created: int
    id: str
    model: str
    object: Literal["chat.completion"]
    usage: Usage
    system_fingerprint: Optional[str] = None

class MessageStream(BaseModel):
    role: Optional[Literal["system", "user", "assistant"]] = None
    content: Optional[str] = None

class ChoiceStream(BaseModel):
    delta: MessageStream
    index: int
    finish_reason: Literal["stop", "max_tokens", "timeout",None,"length"]
class ChatCompletionStreamResponse(BaseModel):
    choices: List[ChoiceStream]
    created: int
    id: str
    model: str
    object: Literal["chat.completion.chunk"]
    usage: Optional[Usage]=None
    system_fingerprint: Optional[str] = None

