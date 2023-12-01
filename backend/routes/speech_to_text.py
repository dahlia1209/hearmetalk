from flask import Blueprint, request, jsonify, session, current_app,Response
from services import openai_services,azure_services
import os,io,tempfile,base64
from models.speech_to_text import AudioDataDto,AudioData
from pydub import AudioSegment
from werkzeug.datastructures import FileStorage

speech_to_text = Blueprint('speech_to_text', __name__)

@speech_to_text.route("/speech_to_text", methods=['POST'])
def speech_to_text_endpoint()->Response:
    # ファイルがリクエストに含まれているか確認
    if 'file' not in request.files:
        return 'ファイルがありません', 400
    file = request.files['file']

    # ファイルが実際に選択されているか、またはファイル名が空でないか確認
    if file.filename == '':
        return 'ファイルが選択されていません', 400
    
    file_basename, file_extension = os.path.splitext(file.filename)
    file_extension = file_extension[1:].lower()
    if file_extension not in ['wav', 'mp4', 'webm']:
        return '許可されていないファイル形式です', 400

    # WAVに変換とBase64エンコードを同時に行う
    wav_audio, encoded_audio_data_with_base64 = convert_and_encode_to_wav(file=file,file_extension=file_extension)
    wav_file_name = file_basename + ".wav"
    audio_data_dto = AudioDataDto(
        encoded_data=encoded_audio_data_with_base64,
        duration_ms=len(wav_audio),
        filename=wav_file_name,
        mime_type="audio/wav",
        file_extension=file_extension
    )

    audio_data=AudioData(
        audio_data_dto=audio_data_dto,
        audio_segment=wav_audio
    )

    # Azure Speech SDKを使ってテキスト変換
    recognition_result =azure_services.transcribe(audio_data)
    audio_data.audio_data_dto.text=recognition_result

    #return 
    return jsonify(audio_data.audio_data_dto.model_dump()), 200

def convert_and_encode_to_wav(file: FileStorage,file_extension:str):
    file_stream = file.stream.read()
    file.stream.seek(0)  # ファイルポインタをリセット
    file_stream_io = io.BytesIO(file_stream)

    # Convert to WAV using ffmpeg
    converted_audio = AudioSegment.from_file(file_stream_io, format=file_extension).set_frame_rate(16000).set_channels(1).set_sample_width(2)

    # Base64エンコードを適用
    buffer = io.BytesIO()
    converted_audio.export(buffer, format="wav")
    buffer.seek(0)
    audio_bytes = buffer.read()
    encoded_audio = base64.b64encode(audio_bytes).decode('utf-8')

    return converted_audio, encoded_audio