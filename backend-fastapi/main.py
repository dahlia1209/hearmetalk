from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from services import openai_services
from typing import List
import time

# from models.chat import ChatCompletionSettings
from models import chat as chat_model
from models import assistant as assistant_model
from dotenv import load_dotenv
from starlette.responses import StreamingResponse
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
import os

load_dotenv()
app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}


@app.post("/chat_stream")
async def chat_stream(chat_completion_settings: chat_model.ChatCompletionSettings):
    print(chat_completion_settings)
    try:
        chat_completion_response = openai_services.chat_completions_create_stream(
            chat_completion_settings
        )

        async def generate():
            async for response in chat_completion_response:
                if response.choices[0].delta.content is not None:
                    yield response.choices[0].delta.content

        return StreamingResponse(generate())
    except ValueError:
        return ({"error": "Text not provided"}, 400)


# @app.post("/assistant_stream")
# async def chat_stream(chat_completion_settings: assistantChatCompletionSettings):
#     print(chat_completion_settings)
#     try:
#         chat_completion_response = openai_services.chat_completions_create_stream(
#             chat_completion_settings
#         )

#         async def generate():
#             async for response in chat_completion_response:
#                 if response.choices[0].delta.content is not None:
#                     yield response.choices[0].delta.content

#         return StreamingResponse(generate())
#     except ValueError:
#         return ({"error": "Text not provided"}, 400)


@app.post("/assistant_init")
async def assistant_init(config: assistant_model.AssistantsCreate):
    print(config)
    try:
        assistant = openai_services.create_assistant(config)
        assistant = openai_services.create_thread()

    except ValueError:
        return ({"error": "Text not provided"}, 400)


# Assuming you have set your OpenAI API key in the environment variables or elsewhere
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


@app.post("/solve_equation")
async def solve_equation(message: assistant_model.Message):
    assistants_create_config = assistant_model.AssistantsCreate(
        instructions="You are a friend. You reply in Japanese. You reply with the content of daily conversation.",
        model="gpt-4",
    )
    assistant = client.beta.assistants.create(**assistants_create_config.model_dump())
    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role=message.role,
        content=message.content,
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while run.status in ["queued", "in_progress", "cancelling"]:
        time.sleep(0.5)  # Wait for 1 second
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print(messages)
    else:
        print(run.status)

    return "completed"
