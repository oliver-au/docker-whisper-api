from flask import Flask, request, jsonify
import whisper
import os
import ffmpeg

app = Flask(__name__)
model = whisper.load_model("medium")  # Use the model that suits your needs

def extract_audio_from_video(video_path, audio_path):
    """Extract audio from video file."""
    try:
        ffmpeg.input(video_path).output(audio_path).run(quiet=True, overwrite_output=True)
    except ffmpeg.Error as e:
        raise Exception(f"Failed to extract audio: {e}")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio or video file provided'}), 400

    file = request.files['audio']
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # Determine the file type
    file_ext = file.filename.rsplit('.', 1)[-1].lower()
    if file_ext in ['mp4', 'mkv', 'avi', 'mov']:  # Add more video formats as needed
        audio_path = file_path.rsplit('.', 1)[0] + '.wav'
        extract_audio_from_video(file_path, audio_path)
    else:
        audio_path = file_path  # Assume it's already an audio file

    try:
        # Transcribe audio file using Whisper
        result = model.transcribe(audio_path)
        os.remove(file_path)  # Clean up the uploaded file
        if audio_path != file_path:
            os.remove(audio_path)  # Clean up the extracted audio file
        return jsonify({'transcript': result['text']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(host='0.0.0.0', port=5001)