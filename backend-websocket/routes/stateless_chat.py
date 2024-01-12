from flask import Blueprint, request, jsonify, session, current_app,Response,stream_with_context
from services import openai_services
import uuid
import os
from models.chat import ChatCompletionSettings,Message,MessageDto,ChatCompletionResponse
import logging
import json

logging.basicConfig(level=logging.debug)
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

@stateless_chat.route("/stateless_chat_stream", methods=['POST'])
def stateless_chat_stream_with_assistant()->Response:
    data = request.get_json(force=True)
    try:
        chat_completion_settings = ChatCompletionSettings(**data)
        logger.info(chat_completion_settings)
        chat_completion_stream_response=openai_services.chat_completions_create_stream(chat_completion_settings)
        def generate():
            for response in chat_completion_stream_response:
                if response.choices[0].delta.content is not None:
                    # logger.info(response.choices[0].delta.content)
                    yield response.choices[0].delta.content  
        return Response(stream_with_context(generate()), content_type='application/json')
    except Exception as e:
        # エラー処理
        return jsonify({"error": str(e)}), 500
