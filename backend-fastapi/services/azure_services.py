import os,tempfile,threading,logging,time,io
import azure.cognitiveservices.speech as speechsdk
from models.speech_to_text import AudioData,AudioDataDto
from flask import current_app
from pydub import AudioSegment
import queue,base64
from io import BytesIO
import app


def initialize_azure_speech_client(speech_recognition_language='ja-JP',speech_synthesis_voice_name='ja-JP-NanamiNeural'):
    """Azureの音声クライアントを初期化します。"""
    speech_key, service_region = os.getenv('AZURE_SPEECH_KEY'), os.getenv('AZURE_SERVICE_REGION')
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3)
    speech_config.speech_recognition_language = speech_recognition_language
    speech_config.speech_synthesis_voice_name = speech_synthesis_voice_name
    return speech_config

def transcribe(audio_data:AudioData)->str:
    """Azureを使用して音声データをテキストに変換する関数。"""
    # 音声データを一時ファイルに保存
    temp_audio_file=tempfile.NamedTemporaryFile(delete=False, suffix=audio_data.audio_data_dto.file_extension )
    audio_data.audio_segment.export(temp_audio_file.name, format="wav")

    speech_config = initialize_azure_speech_client()
    audio_input = speechsdk.AudioConfig(filename=temp_audio_file.name)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        return f"Speech Recognition canceled: {cancellation.reason}"

def synthesize(text:str,speech_synthesis_voice_name:str)->bytes:
    """Azureを使用してテキストを音声データに変換する関数。"""
    try:
        speech_config = initialize_azure_speech_client(speech_synthesis_voice_name=speech_synthesis_voice_name)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=None)

        result = speech_synthesizer.speak_text(text)
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            raise Exception(f"Speech synthesis canceled: {cancellation.reason}")
            
    except Exception as e:
        # 例外が発生した場合のエラーハンドリング
        print(f"An error occurred: {e}")
        # 必要に応じて、Noneを返すか、エラーを再度スローする
        return None

def recognize(audio_file):
    """Azureを使用して音声データから指定された情報や意図を認識する関数（例: 音声コマンドの認識）。"""
    # この関数はtranscribeと似ていますが、より高度な音声認識の機能を実装する場合に使用します。
    # ここでは基本的なトランスクリプションと同じコードを再利用します。
    return transcribe(audio_file)


def push_stream_writer(stream, audio_queue,format,temp_file):
    END_OF_STREAM_MARKER = None

    def write(stream:speechsdk.audio.PushAudioInputStream,audio_data:bytes):
        # byte_stream_input = BytesIO(audio_data)
    
        # AudioSegment オブジェクトを作成
        # この例ではデータがWAVフォーマットであると仮定
        # audio_segment = AudioSegment.from_file(byte_stream_input, format=format)

        # # 必要に応じてオーディオデータを変換（サンプルレート、チャンネル数、サンプル幅を設定）
        # audio_segment = audio_segment.set_frame_rate(16000).set_channels(1).set_sample_width(2)

        # # メモリ上でオーディオデータのエクスポートを行い、ストリームへ書き込む
        # byte_stream = BytesIO()
        # audio_segment.export(byte_stream, format='wav')
        # audio_bytes = byte_stream.getvalue()
        # stream.write(audio_bytes)

        # print(temp_file.name)
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

def start_speech_recognition(file_format:str)->(speechsdk.SpeechRecognizer,threading.Thread,queue.Queue):
    def recognized_handler(evt):
        # 認識が完了したときの処理
        print(f"認識結果: {evt.result.text}")
        # print('recognized_handler',str(socketio))
        # socketio.emit('message','recognized_handler')
        #debug
        # if threading.current_thread() == threading.main_thread():
        #     print("recognized_handler is the main thread.")
        # else:
        #     print("recognized_handler is not the main thread.")
        app.reconized_message_emit(evt.result.text)
        # print('recognized_handler')


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
    # print('start_speech_recognition',session_id)
    # print('start_speech_recognition',str(socketio))
    # socketio.emit('message','start_speech_recognition')
    speech_recognizer.recognized.connect(lambda evt: recognized_handler(evt))
    speech_recognizer.recognizing.connect(recognizing_handler)
    speech_recognizer.canceled.connect(canceled_handler)
    speech_recognizer.session_started.connect(session_started_handler)
    speech_recognizer.session_stopped.connect(session_stopped_handler)

    push_stream_writer_thread = threading.Thread(target=push_stream_writer, args=(stream,audio_queue,file_format,temp_file))
    push_stream_writer_thread.start()
    
    #debug
    # if threading.current_thread() == threading.main_thread():
    #     print("start_speech_recognition is the main thread.")
    # else:
    #     print("start_speech_recognition is not the main thread.")
    print('start_speech_recognitionからの呼び出し')
    socketio.emit('message','start_speech_recognitionからの呼び出し')


    speech_recognizer.start_continuous_recognition()
    return speech_recognizer, push_stream_writer_thread,audio_queue

def stop_speech_recognition(speech_recognizer:speechsdk.SpeechRecognizer,push_stream_writer_thread:threading.Thread,audio_queue:queue.Queue):
    audio_queue.put((None,2,2000))
    speech_recognizer.stop_continuous_recognition()
    push_stream_writer_thread.join()
    
