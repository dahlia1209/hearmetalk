from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from routes import transcription, synthesis, chat, orchestration
import os

# ログの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = os.getenv('APP_CONFIG_SECRET_KEY') 

# 各ルートのBlueprintを登録
app.register_blueprint(transcription.transcription)
app.register_blueprint(synthesis.synthesis)
app.register_blueprint(chat.chat)
app.register_blueprint(orchestration.orchestration)

if __name__ == '__main__':
    app.run(debug=True)
