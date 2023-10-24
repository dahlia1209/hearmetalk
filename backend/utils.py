import os
import time

# 安全にファイルを削除する関数
def safe_remove(file_path, retry=5, delay=1):
    for _ in range(retry):
        try:
            os.remove(file_path)
            return
        except PermissionError:
            time.sleep(delay)
    raise PermissionError(f"Failed to remove file: {file_path} after {retry} retries.")
