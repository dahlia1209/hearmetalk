from flask import Blueprint, jsonify, request, Response, current_app, session
import requests
import uuid
from routes import chat,synthesis,transcription

orchestration = Blueprint('orchestration', __name__)

@orchestration.route('/orchestrate', methods=['POST'])
def orchestrate_route():
    # セッションからユーザーIDを取得、存在しなければ新しいIDを生成
    session_id = session.get('session_id') or str(uuid.uuid4())
    session['session_id'] = session_id

    # 1. 音声をテキストに変換
    audio_data = request.files['audio'].read()
    response_transcribe = transcription.process_and_recognize_speech(audio_data)

    # 2. OpenAIからのレスポンスを取得
    response_chat = chat.chat_logic(response_transcribe)

    # 3. テキストを音声データに変換
    response_synthesize = synthesis.synthesize_speech_from_text(response_chat)

    return Response(response_synthesize, mimetype="audio/wav")
