from flask import Blueprint, request, jsonify, session, current_app,Response
from services import openai_services,azure_services
import os,io,tempfile,base64
from models.speech_to_text import AudioDataDto,AudioData
from models.text_to_speech import Speaker
from pydub import AudioSegment
from werkzeug.datastructures import FileStorage

text_to_speech = Blueprint('text_to_speech', __name__)

@text_to_speech.route("/text_to_speech", methods=['POST'])
def text_to_speech_endpoint()->Response:
    # リクエストボディ取得
    request_data = request.get_json()
    audio_data_dto = AudioDataDto(**request_data['audioDataDto'])
    speaker = Speaker(**request_data['speaker'])
    current_app.logger.info(audio_data_dto)
    current_app.logger.info(speaker)
    
    # Azure Speech SDKを使ってオーディオデータに変換
    # target_format=audio_data_dto.file_extension.replace('.','') #「.」を除外
    audio_data_dto.file_extension='.mp3'
    audio_data_dto.mime_type='audio/mpeg'
    audio_data_bytes =azure_services.synthesize(audio_data_dto.text,speaker.synthesis_voice_name) 
    audio_data_dto.encoded_data=convert_and_encode_audio(audio_data_bytes,'mp3')

    #return 
    return jsonify(audio_data_dto.model_dump(by_alias=True)), 200

def convert_and_encode_audio(audio_data_bytes: bytes, target_format: str) -> str:
    """
    Bytes形式のオーディオデータを指定したMIMEタイプに変換し、Base64でエンコードする。

    :param audio_data_bytes: 変換するオーディオデータ（bytes形式）
    :param target_format: 変換するオーディオフォーマット（例: 'mp3', 'wav'）
    :return: Base64エンコードされたオーディオデータ
    """
    # BytesIOを使って、bytesデータからオーディオを読み込む
    audio = AudioSegment.from_file(io.BytesIO(audio_data_bytes))

    # BytesIOオブジェクトを作成し、そこに変換されたオーディオを書き込む
    buffer = io.BytesIO()
    audio.export(buffer, format=target_format)
    
    # Base64でエンコード
    encoded_audio = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return encoded_audio