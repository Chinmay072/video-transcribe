import os
import assemblyai as aai
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set AssemblyAI API key directly
aai.settings.api_key = "7560a6e22bce49dd894e33484c468c58"

# Configure upload folder
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'm4a', 'webm'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_transcription(file_path):
    # Create a transcriber object
    transcriber = aai.Transcriber()
    
    # Transcribe the audio file
    transcript = transcriber.transcribe(file_path)
    
    # Process the transcript into sentences
    sentences = []
    current_sentence = ""
    start_time = None
    
    for word in transcript.words:
        if not current_sentence:
            start_time = word.start / 1000.0
        
        current_sentence += word.text + " "
        
        if word.text.endswith((".", "!", "?")):
            sentences.append({
                "text": current_sentence.strip(),
                "start_time": start_time,
                "end_time": word.end / 1000.0
            })
            current_sentence = ""
            start_time = None
    
    return sentences

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the transcription
        sentences = process_transcription(filepath)
        
        # Clean up the uploaded file
        os.remove(filepath)
        
        return jsonify({
            "success": True,
            "sentences": sentences
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
