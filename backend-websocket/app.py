import eventlet
eventlet.monkey_patch()

from flask import Flask,Response,stream_with_context,jsonify,request
from flask_socketio import SocketIO,send, emit
from flask_cors import CORS
from dotenv import load_dotenv
import logging,base64,io,os
from models.ai_talk import ServerEvents,ClientEvents
from models.chat import ChatCompletionSettings,Message,MessageDto,ChatCompletionResponse
from routes import stateless_chat
from services import openai_services
import time
import queue
import threading,tempfile
from models.speech_to_text import AudioDataDto,AudioData
from pydub import AudioSegment
from werkzeug.datastructures import FileStorage
from io import BytesIO
import azure.cognitiveservices.speech as speechsdk

#debug
connected_users = []


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# .envファイルから環境変数を読み込む
load_dotenv()
recognition_thread = None

@socketio.on('connect')
def handle_connect():
    session_id = request.sid
    print('connected',session_id)
    connected_users.append(session_id)

@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    print('Client disconnected')
    connected_users.remove(session_id)

@socketio.on('message')
def handle_message(data):
    logger.info('received message:'+data)
    my_list = [1, 2, 3, 4, 5]
    for item in my_list:
        time.sleep(1)
        socketio.emit('message','received your message:'+str(item))
        # eventlet.sleep(0)
        socketio.sleep(0)
    # thread=threading.Thread(target=background_thread, daemon=True)
    # thread=threading.Thread(target=background_thread)
    # thread.start()
    # thread.join()
    # test_func()
    # background_thread()

def test_func():
    def thread_func():
        print('thread_func waiting for 2 sec')
        socketio.emit('message','thread_func')
        time.sleep(2)
        print('thread_func done')
    
    thread=threading.Thread(target=thread_func)
    socketio.emit('message','test_func')
    thread.start()
    thread.join()

def background_thread():
    """ 1秒ごとにクライアントにメッセージを送信するバックグラウンドスレッド """
    count = 0
    while True:
        time.sleep(1)  # 1秒待機
        count += 1
        # print({'data': f'Message {count}'})
        print('connected_users:',connected_users)
        socketio.emit('message', f'Message {count}')
        socketio.sleep(0)
        # test_func()

@socketio.on(ServerEvents.PROMPT_MESSAGE)
def handle_message(data):
    chat_completion_settings = ChatCompletionSettings(**data)
    logger.info(chat_completion_settings.model_dump_json())
    try:
        chat_completion_settings = ChatCompletionSettings(**data)
        logger.info(chat_completion_settings)
        chat_completion_stream_response=openai_services.chat_completions_create_stream(chat_completion_settings)
        for response in chat_completion_stream_response:
            if response.choices[0].delta.content is not None:
                socketio.emit('response_message',response.choices[0].delta.content)
                socketio.sleep(0)
    
    except Exception as e:
        # エラー処理
        return jsonify({"error": str(e)}), 500




# Global variables
speech_recognizer = None
audio_queue = None
push_stream_writer_thread = None
file_format=None
audio_data = BytesIO()
audio_segment=None
temp_file = None
# session_id=None

@socketio.on('start_recognition')
def handle_start_recognition(supported_file_format:str):
    global speech_recognizer, push_stream_writer_thread,audio_queue,file_format,audio_data,audio_segment,temp_file
    file_format=supported_file_format
    # session_id = request.sid
    # print('start_recognition',session_id)
    speech_recognizer, push_stream_writer_thread,audio_queue=start_speech_recognition(file_format)
    
    socketio.emit( 'is_recognition_ready',True)
    socketio.emit( 'message','is_recognition_ready')
    logger.info('start_recognition')
    reconized_message_emit('start_recognitionからの呼び出し')
    

    # audio_data.seek(0)
    # logger.info(temp_file.name)

@socketio.on('recording_audio')
def handle_audio_data(recieved_audio_data:bytes,received_chunk_count:int,received_time_slice):
    global audio_queue
    # socketio.emit( 'message','recording_audio')
    # reconized_message_emit('recording_audioからの呼び出し')

    if audio_queue:


        audio_queue.put((recieved_audio_data,received_chunk_count,received_time_slice))

def reconized_message_emit(message:str):
    print('reconized_message_emit:',message)
    socketio.emit('message',message)
    socketio.sleep(0)


@socketio.on('stop_recognition')
def handle_stop_recognition():
    global speech_recognizer, push_stream_writer_thread,audio_queue,audio_segment,audio_data,file_format
    stop_speech_recognition(speech_recognizer, push_stream_writer_thread,audio_queue)
    socketio.emit( 'is_recognition_ready',False)
    socketio.sleep(0)
    logger.info('stop_recognition')
    socketio.emit('message','stop_recognition')





def push_stream_writer(stream, audio_queue,format,temp_file):
    END_OF_STREAM_MARKER = None

    def write(stream:speechsdk.audio.PushAudioInputStream,audio_data:bytes):

        temp_file.write(audio_data)
        byte_stream = BytesIO()
        audio_segment = AudioSegment.from_file(temp_file.name, format=format).set_frame_rate(16000).set_channels(1).set_sample_width(2)
        start_time = (chunk_count-1)*time_slice  # 開始時間（ミリ秒単位）
        end_time = chunk_count*time_slice    # 終了時間（ミリ秒単位）
        extract_audio_segment = audio_segment[start_time:end_time]
        extract_audio_segment.export(byte_stream, format="wav")
        audio_bytes = byte_stream.getvalue()
        stream.write(audio_bytes)

    while True:
        try:
            audio_data,chunk_count,time_slice = audio_queue.get()

            # 終了マーカーを受け取ったらループを終了
            if audio_data is END_OF_STREAM_MARKER:
                temp_file.close()
                
                #デバッグ用エクスポート
                audio_segment = AudioSegment.from_file(temp_file.name, format=format).set_frame_rate(16000).set_channels(1).set_sample_width(2)
                start_time = (chunk_count-1)*time_slice  # 開始時間（ミリ秒単位）
                end_time = chunk_count*time_slice    # 終了時間（ミリ秒単位）
                extract_audio_segment = audio_segment[start_time:end_time]
                extract_audio_segment.export("received_audio.wav", format="wav")
                # audio_segment.export("received_audio.wav", format="wav")

                os.remove(temp_file.name)
                break

            # ストリームにデータを書き込む
            write(stream,audio_data)

        except Exception as e:
            # エラーハンドリング
            print(f"エラー発生: {e}")
            break
        
    stream.close()
    
def initialize_azure_speech_client(speech_recognition_language='ja-JP',speech_synthesis_voice_name='ja-JP-NanamiNeural'):
    """Azureの音声クライアントを初期化します。"""
    speech_key, service_region = os.getenv('AZURE_SPEECH_KEY'), os.getenv('AZURE_SERVICE_REGION')
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3)
    speech_config.speech_recognition_language = speech_recognition_language
    speech_config.speech_synthesis_voice_name = speech_synthesis_voice_name
    return speech_config
    
def start_speech_recognition(file_format:str)->(speechsdk.SpeechRecognizer,threading.Thread,queue.Queue):
    def recognized_handler(evt):
        # 認識が完了したときの処理
        print(f"認識結果: {evt.result.text}")
        # reconized_message_emit('recognized_handlerからの通知')
        # socketio.emit('message','recognized_handlerからの通知')


    def recognizing_handler(evt):
        # 認識中の処理（例: リアルタイムでの部分的な認識結果）
        print(f"途中結果: {evt.result.text}")


    def canceled_handler(evt):
        # エラー発生時の処理
        print(f"認識キャンセル: {evt.reason}")

    def session_started_handler(evt):
        # エラー発生時の処理
        print(f"セッション開始しました。: {evt}")

    def session_stopped_handler(evt):
        # エラー発生時の処理
        print(f"セッション終了しました。: {evt}")

    speech_config = initialize_azure_speech_client()
    stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    audio_queue = queue.Queue()
    temp_file = tempfile.NamedTemporaryFile(delete=False,mode='wb')

    # 認識結果のイベントハンドラを設定
    speech_recognizer.recognized.connect(lambda evt: recognized_handler(evt))
    speech_recognizer.recognizing.connect(recognizing_handler)
    speech_recognizer.canceled.connect(canceled_handler)
    speech_recognizer.session_started.connect(session_started_handler)
    speech_recognizer.session_stopped.connect(session_stopped_handler)

    push_stream_writer_thread = threading.Thread(target=push_stream_writer, args=(stream,audio_queue,file_format,temp_file))
    push_stream_writer_thread.start()

    print('start_speech_recognitionからの呼び出し')
    reconized_message_emit('start_speech_recognitionからの呼び出し')

    speech_recognizer.start_continuous_recognition()
    return speech_recognizer, push_stream_writer_thread,audio_queue

def stop_speech_recognition(speech_recognizer:speechsdk.SpeechRecognizer,push_stream_writer_thread:threading.Thread,audio_queue:queue.Queue):
    audio_queue.put((None,2,2000))
    speech_recognizer.stop_continuous_recognition()
    push_stream_writer_thread.join()
    print('stop_speech_recognition done')

if __name__ == '__main__':
    # threading.Thread(target=background_thread, daemon=True).start()
    socketio.run(app)

