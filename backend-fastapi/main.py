from fastapi import FastAPI,WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
from services import openai_services
import uuid
import os
from models.chat import ChatCompletionSettings,Message,MessageDto
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

origins = [
    "http://localhost:8080",
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

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        json_data = json.loads(data)
        print(json_data)
        chat_completion_settings = ChatCompletionSettings(**json_data)
        chat_completion_stream_response=openai_services.chat_completions_create_stream(chat_completion_settings)
        for response in chat_completion_stream_response:
            if response.choices[0].delta.content is not None:
                # print(response.choices[0].delta.content)
                await websocket.send_text(response.choices[0].delta.content)

