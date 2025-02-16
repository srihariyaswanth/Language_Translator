import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from deep_translator import GoogleTranslator
from gtts import gTTS
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all origins

AUDIO_DIR = 'static/audio'
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid request: Missing text'}), 400

    spoken_text = data['text']
    src_lang = data.get('src', 'en')
    dest_lang = data.get('dest', 'ta')

    try:
        translated_text = GoogleTranslator(source=src_lang, target=dest_lang).translate(spoken_text)
        audio_file_path = os.path.join(AUDIO_DIR, 'translated_speech.mp3')
        tts = gTTS(translated_text, lang=dest_lang)
        tts.save(audio_file_path)
        return jsonify({'translatedText': translated_text, 'audioUrl': '/audio/translated_speech.mp3'})
    except Exception as e:
        print(f"Error during translation: {str(e)}")
        return jsonify({'error': f"Translation failed: {str(e)}"}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
