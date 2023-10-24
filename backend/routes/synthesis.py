from flask import Blueprint, request, jsonify, Response
from services import azure_services

synthesis = Blueprint('synthesis', __name__)

@synthesis.route('/synthesize', methods=['POST'])
def synthesize_text():
    data = request.get_json(force=True)
    text = data.get('text')

    try:
        synthesized_audio = synthesize_speech_from_text(text)
        return Response(synthesized_audio, mimetype="audio/wav")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

def synthesize_speech_from_text(text):
    """
    Given a text, synthesize it into speech using Azure services.
    :param text: The text to synthesize.
    :return: The synthesized audio.
    """
    if not text:
        raise ValueError("Text not provided")
    
    synthesized_audio = azure_services.synthesize(text)
    return synthesized_audio
