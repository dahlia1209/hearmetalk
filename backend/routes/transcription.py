from flask import Blueprint, request, jsonify, current_app
import tempfile
import subprocess
from services import azure_services
import utils

transcription = Blueprint('transcription', __name__)

@transcription.route('/recognize', methods=['POST'])
def recognize_speech_route():
    audio_data = request.files['audio'].read()

    # ログ出力
    current_app.logger.info(f"Audio data size: {len(audio_data)} bytes")

    recognition_result = process_and_recognize_speech(audio_data)

    # 認識結果のログ出力
    current_app.logger.info(f"Recognition result: {recognition_result}")

    return jsonify({"text": recognition_result})

def process_and_recognize_speech(audio_data):
    # 音声データを一時ファイルに保存
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")
    audio_file.write(audio_data)
    audio_file.close()

    # Convert WebM to WAV using ffmpeg
    wav_file_name = audio_file.name.replace('.webm', '.wav')
    command = ['ffmpeg', '-i', audio_file.name, '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', wav_file_name]
    subprocess.run(command, check=True)

    # Azure Speech SDKを使ってテキスト変換
    recognition_result = azure_services.transcribe(wav_file_name)

    #ファイル削除
    utils.safe_remove(wav_file_name)
    utils.safe_remove(audio_file.name)

    return recognition_result