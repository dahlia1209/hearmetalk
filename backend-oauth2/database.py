from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import load_dotenv
load_dotenv()

# 環境変数からSQL Serverデータベース接続URLを取得
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# ユーザーデータベース名
DATABASE_NAME = "hearmetalk"

# autocommitモードでマスターデータベースを使用してエンジンを作成
master_engine = create_engine(SQLALCHEMY_DATABASE_URL, isolation_level="AUTOCOMMIT")

# ユーザーデータベースの存在を確認し、存在しない場合は作成
with master_engine.connect() as conn:
    result = conn.execute(text(f"SELECT db_id('{DATABASE_NAME}')"))
    db_id = result.scalar()
    if db_id is None:
        conn.execute(text(f"CREATE DATABASE {DATABASE_NAME}"))
        print(f"Database '{DATABASE_NAME}' created successfully.")
    else:
        print(f"Database '{DATABASE_NAME}' already exists.")

# 通常の操作用にユーザーデータベース用のエンジンを作成
user_database_url = SQLALCHEMY_DATABASE_URL.replace('master', DATABASE_NAME)
engine = create_engine(user_database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
