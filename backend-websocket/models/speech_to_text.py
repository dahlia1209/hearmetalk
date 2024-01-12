from typing import Literal,Optional,List,Any
from pydantic import BaseModel,Field
from werkzeug.datastructures import FileStorage
from pydub import AudioSegment


class AudioDataDto(BaseModel):
    encoded_data: str=Field(..., alias='encodedData')
    duration_ms : int=Field(..., alias='durationMs')
    filename: str=Field(..., alias='filename')
    mime_type: str=Field(..., alias='mimeType')
    file_extension:str=Field(..., alias='fileExtension')
    text:str=Field("", alias='text')
    class Config:
        populate_by_name = True

class AudioData(BaseModel):
    audio_data_dto:AudioDataDto
    audio_segment:AudioSegment

    class Config:
        arbitrary_types_allowed = True
