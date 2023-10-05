from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask import Response
from flask import Flask, request, jsonify
import azure.cognitiveservices.speech as speechsdk
import tempfile
import os
import time
import openai
from dotenv import load_dotenv
import logging
import uuid
import requests 

# ログの設定
logging.basicConfig(level=logging.DEBUG)  # この行を変更することでログレベルを変えられます
logger = logging.getLogger(__name__)

# .envファイルから環境変数を読み込む
load_dotenv()  

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/api/message', methods=['GET'])
def get_message():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_file = tempfile.NamedTemporaryFile(delete=False)
    audio_data = request.files['audio'].read()
    audio_file.write(audio_data)
    audio_file.close()

    speech_key, service_region = os.getenv('SPEECH_KEY'), "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = 'ja-JP'
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file.name)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # 認識結果を保存するためのリスト
    results = []

    # イベントハンドラで認識結果をリストに追加する
    def recognized(args):
        results.append(args.result.text)

    speech_recognizer.recognized.connect(recognized)

    # 連続的な音声認識を開始
    speech_recognizer.start_continuous_recognition()
    time.sleep(10) 
    speech_recognizer.stop_continuous_recognition()
    del speech_recognizer 
    time.sleep(2)  

    # ファイル削除の試み
    try:
        os.unlink(audio_file.name)  # 一時ファイルの削除
    except PermissionError:
        time.sleep(5)  # さらに待機して再試行
        os.unlink(audio_file.name) 

    print("Temp file saved at:", audio_file.name)

    # 結果を結合して返す
    transcription = " ".join(results)
    return jsonify({"transcription": transcription})

@app.route('/synthesize', methods=['POST'])
def synthesize():
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_key = os.getenv('SPEECH_KEY')
    service_region = "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Note: the voice setting will not overwrite the voice element in input SSML.
    speech_config.speech_synthesis_voice_name = "ja-JP-AoiNeural"
    data = request.get_json(force=True)
    text = data.get('text')

    if not text:
        return jsonify({"error": "Text not provided"}), 400

    # use the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    # result = speech_synthesizer.speak_text_async(text).get()
    result = speech_synthesizer.speak_text_async(text).get()

    # return jsonify({"error": "Unknown error occurred"}), 500
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # Return the synthesized audio data directly.
        return Response(result.audio_data, mimetype="audio/wav")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        error_message = "Speech synthesis canceled: {}".format(cancellation_details.reason)
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            error_message += "\nError details: {}".format(cancellation_details.error_details)
        return jsonify({"error": error_message}), 500

    return jsonify({"error": "Unknown error occurred"}), 500

# 対話履歴を保存するためのディクショナリ
user_chat_histories = {}
app.config['SECRET_KEY'] = os.getenv('APP_CONFIG_SECRET_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    openai.api_key = os.getenv('OPENAI_API_KEY')
    data = request.get_json(force=True)
    user_input = data.get('text')

    # ログに出力
    logger.debug(f"Received data: {data}")

    if not user_input:
        return jsonify({"error": "Text not provided"}), 400

    # セッションからユーザーIDを取得、存在しなければ新しいIDを生成
    session_id = session.get('session_id') or str(uuid.uuid4())
    session['session_id'] = session_id

    logger.debug(f"session_id: {session_id}")

    if session_id not in user_chat_histories:
        user_chat_histories[session_id] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # ユーザーの入力を対話履歴に追加
    user_chat_histories[session_id].append({"role": "user", "content": user_input})

    # OpenAIにクエリを投げる
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=user_chat_histories[session_id]
    )

    # OpenAIへのリクエスト内容をログに出力
    logger.debug(f"Sent to OpenAI: {user_chat_histories[session_id]}")

    response_text = completion.choices[0].message["content"]
    # レスポンス内容をログに出力
    logger.debug(f"Received from OpenAI: {response_text}")

    # アシスタントのレスポンスを対話履歴に追加
    user_chat_histories[session_id].append({"role": "assistant", "content": response_text})

    return jsonify({"text": response_text})

@app.route('/orchestrate', methods=['POST'])
def orchestrate():
    # 1. 音声をテキストに変換
    audio_data = request.files['audio']
    response_transcribe = requests.post('http://localhost:5000/transcribe', files={'audio': audio_data})

    if response_transcribe.status_code != 200:
        return jsonify({"error": "Failed to transcribe audio"}), 500

    transcription = response_transcribe.json().get('transcription')

    # 2. OpenAIからのレスポンスを取得
    response_chat = requests.post('http://localhost:5000/chat', json={"text": transcription})
    if response_chat.status_code != 200:
        return jsonify({"error": "Failed to chat"}), 500

    response_text = response_chat.json().get('text')

    # 3. テキストを音声データに変換
    response_synthesize = requests.post('http://localhost:5000/synthesize', json={"text": response_text})
    if response_synthesize.status_code != 200:
        return jsonify({"error": "Failed to synthesize voice"}), 500

    return Response(response_synthesize.content, mimetype="audio/wav")

if __name__ == '__main__':
    app.run(debug=True)
