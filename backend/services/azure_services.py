import os
import azure.cognitiveservices.speech as speechsdk

def initialize_azure_speech_client():
    """Azureの音声クライアントを初期化します。"""
    speech_key, service_region = os.getenv('AZURE_SPEECH_KEY'), os.getenv('AZURE_SERVICE_REGION')
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = os.getenv('AZURE_SPEECH_RECOGNITION_LANGUAGE')
    speech_config.speech_synthesis_voice_name = os.getenv('AZURE_SPEECH_SYNTHESIS_VOICE_NAME')
    return speech_config

def transcribe(audio_file):
    """Azureを使用して音声データをテキストに変換する関数。"""
    speech_config = initialize_azure_speech_client()
    audio_input = speechsdk.AudioConfig(filename=audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        return f"Speech Recognition canceled: {cancellation.reason}"

def synthesize(text):
    """Azureを使用してテキストを音声データに変換する関数。"""
    speech_config = initialize_azure_speech_client()
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = speech_synthesizer.speak_text(text)
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        return f"Speech synthesis canceled: {cancellation.reason}"

def recognize(audio_file):
    """Azureを使用して音声データから指定された情報や意図を認識する関数（例: 音声コマンドの認識）。"""
    # この関数はtranscribeと似ていますが、より高度な音声認識の機能を実装する場合に使用します。
    # ここでは基本的なトランスクリプションと同じコードを再利用します。
    return transcribe(audio_file)
