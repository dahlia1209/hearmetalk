from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from routes import transcription, synthesis, chat, orchestration,stateless_chat,speech_to_text,text_to_speech
import os

# ログの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = os.getenv('APP_CONFIG_SECRET_KEY') 
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

# 各ルートのBlueprintを登録
app.register_blueprint(transcription.transcription)
app.register_blueprint(synthesis.synthesis)
app.register_blueprint(chat.chat)
app.register_blueprint(stateless_chat.stateless_chat)
app.register_blueprint(orchestration.orchestration)
app.register_blueprint(speech_to_text.speech_to_text)
app.register_blueprint(text_to_speech.text_to_speech)

if __name__ == '__main__':
    app.run(debug=True)
