from openai import OpenAI
import os
from models.chat import ChatCompletionSettings,ChatCompletionResponse,ChatCompletionStreamResponse
import logging
from pydantic import  ValidationError
from typing import Generator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def chat_with_openai(messages):

    client = OpenAI()
    client.api_key = os.getenv('OPENAI_API_KEY')
    completion = client.chat.completions.create(
        model=os.getenv('OPENAI_CHATCOMPLETION_MODEL'),
        messages=messages
    )

    return completion.choices[0].message["content"]

def chat_completions_create(chat_completion_settings:ChatCompletionSettings)->ChatCompletionResponse:
    client = OpenAI()
    client.api_key = os.getenv('OPENAI_API_KEY')
    chat_completion_settings_dict = chat_completion_settings.model_dump()
    response = client.chat.completions.create(**chat_completion_settings_dict)
    response_dict=response.model_dump()
    try:
        chat_completion_response=ChatCompletionResponse(**response_dict)
    except ValidationError as e:
        logger.error(f"ValidationError occurred: {e}")

    return chat_completion_response

def chat_completions_create_stream(chat_completion_settings:ChatCompletionSettings)->Generator[ChatCompletionStreamResponse, None, None]:
    client = OpenAI()
    client.api_key = os.getenv('OPENAI_API_KEY')
    chat_completion_settings_dict = chat_completion_settings.model_dump()

    stream = client.chat.completions.create(**chat_completion_settings_dict)
    for chunk in stream:
        try:
            chunk_format=ChatCompletionStreamResponse(**chunk.model_dump())
            yield chunk_format
            # if chunk_format.choices[0].delta.content is not None:
            #     yield chunk_format.choices[0].delta.content
        except ValidationError as e:
            logger.error(f"ValidationError occurred: {e}")

