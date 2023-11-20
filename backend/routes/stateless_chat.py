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

# def stateless_chat_logic(chat_completion_settings:ChatCompletionSettings):
#     if not text_input:
#         raise ValueError("Text not provided")

#     # セッションからユーザーIDを取得、存在しなければ新しいIDを生成
#     session_id = session.get('session_id') or str(uuid.uuid4())
#     session['session_id'] = session_id

#     if session_id not in user_chat_histories:
#         user_chat_histories[session_id] = [
#             {"role": "system", "content": "You are a helpful assistant."}
#         ]

#     # ユーザーの入力を対話履歴に追加
#     user_chat_histories[session_id].append({"role": "user", "content": text_input})

#     # OpenAIにクエリを投げる
#     response_text = openai_services.chat_with_openai(user_chat_histories[session_id])

#     # OpenAIへのリクエスト内容をログに出力
#     current_app.logger.debug(f"Sent to OpenAI: {user_chat_histories[session_id]}")

#     # レスポンス内容をログに出力
#     current_app.logger.debug(f"Received from OpenAI: {response_text}")

#     # アシスタントのレスポンスを対話履歴に追加
#     user_chat_histories[session_id].append({"role": "assistant", "content": response_text})

#     return response_text
