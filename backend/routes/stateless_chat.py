from flask import Blueprint, request, jsonify, session, current_app,Response
from services import openai_services
import uuid
import os
from models.chat import ChatCompletionSettings,Message,MessageDto,ChatCompletionResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stateless_chat = Blueprint('stateless_chat', __name__)

@stateless_chat.route("/stateless_chat", methods=['POST'])
def stateless_chat_with_assistant()->Response:
    data = request.get_json(force=True)
    try:
        chat_completion_settings = ChatCompletionSettings(**data)
        logger.info(chat_completion_settings)
        chat_completion_response=openai_services.chat_completions_create(chat_completion_settings)
        logger.info(chat_completion_response)
        chat_completion_response.choices[0].message

        return jsonify(chat_completion_response.choices[0].message.model_dump())
    except Exception as e:
        # エラー処理
        return jsonify({"error": str(e)}), 500
