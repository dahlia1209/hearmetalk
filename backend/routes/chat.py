from flask import Blueprint, request, jsonify, session, current_app
from services import openai_services
import uuid
import os

chat = Blueprint('chat', __name__)

# 対話履歴を保存するためのディクショナリ
user_chat_histories = {}

@chat.route('/chat', methods=['POST'])
def chat_with_assistant():
    data = request.get_json(force=True)
    user_input = data.get('text')

    try:
        response_text = chat_logic(user_input)
        return jsonify({"text": response_text})
    except ValueError:
        return jsonify({"error": "Text not provided"}), 400

def chat_logic(text_input):
    if not text_input:
        raise ValueError("Text not provided")

    # セッションからユーザーIDを取得、存在しなければ新しいIDを生成
    session_id = session.get('session_id') or str(uuid.uuid4())
    session['session_id'] = session_id

    current_app.logger.debug(f"session_id 1: {session_id}")

    if session_id not in user_chat_histories:
        user_chat_histories[session_id] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # ユーザーの入力を対話履歴に追加
    user_chat_histories[session_id].append({"role": "user", "content": text_input})

    # OpenAIにクエリを投げる
    response_text = openai_services.chat_with_openai(user_chat_histories[session_id])

    # OpenAIへのリクエスト内容をログに出力
    current_app.logger.debug(f"Sent to OpenAI: {user_chat_histories[session_id]}")

    # レスポンス内容をログに出力
    current_app.logger.debug(f"Received from OpenAI: {response_text}")

    # アシスタントのレスポンスを対話履歴に追加
    user_chat_histories[session_id].append({"role": "assistant", "content": response_text})

    return response_text
