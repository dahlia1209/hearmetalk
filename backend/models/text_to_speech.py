from typing import Literal,Optional,List,Any
from pydantic import BaseModel,Field
from werkzeug.datastructures import FileStorage
from pydub import AudioSegment


class Speaker(BaseModel):
    language: str = Field(..., alias='language')
    language_display: str = Field(..., alias='languageDisplay')
    sex: str = Field(..., alias='sex')
    sex_display: str = Field(..., alias='sexDisplay')
    name: str = Field(..., alias='name')
    name_display: str = Field(..., alias='nameDisplay')
    synthesis_voice_name: str = Field(..., alias='synthesisVoiceName')

    class Config:
        populate_by_name = True