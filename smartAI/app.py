from flask import Flask, render_template, request, jsonify
import os
import traceback
import base64
from utils import get_answer, text_to_speech, speech_to_text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'audio_data' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio_data']
        audio_path = "temp_audio.mp3"
        audio_file.save(audio_path)

        transcript = speech_to_text(audio_path)
        os.remove(audio_path)

        return jsonify({'transcript': transcript})
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        data = request.json
        messages = data.get('messages')

        if not messages:
            return jsonify({'error': 'No messages provided'}), 400

        response_text = get_answer(messages)
        audio_file_path = text_to_speech(response_text)
        
        with open(audio_file_path, "rb") as f:
            audio_data = f.read()
        
        audio_base64 = base64.b64encode(audio_data).decode("utf-8")
        os.remove(audio_file_path)

        return jsonify({'response': response_text, 'audio': audio_base64})
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
