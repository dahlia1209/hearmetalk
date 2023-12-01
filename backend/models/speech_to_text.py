from typing import Literal,Optional,List,Any
from pydantic import BaseModel,StrictBytes
from werkzeug.datastructures import FileStorage
from pydub import AudioSegment

class AudioDataDto(BaseModel):
    encoded_data: str
    duration_ms : int
    filename: str
    mime_type: str
    file_extension:str
    text:str=""

class AudioData(BaseModel):
    audio_data_dto:AudioDataDto
    audio_segment:AudioSegment

    class Config:
        arbitrary_types_allowed = True
