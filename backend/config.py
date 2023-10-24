import logging
from dotenv import load_dotenv

# ログの設定
logging.basicConfig(level=logging.DEBUG)  # この行を変更することでログレベルを変えられます

# .envファイルから環境変数を読み込む
load_dotenv()
