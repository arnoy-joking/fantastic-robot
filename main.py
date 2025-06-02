from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

app = Flask(__name__)
CORS(app)

@app.route('/transcript')
def transcript():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Missing video id parameter"}), 400

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([item['text'] for item in transcript_list])
        return jsonify({"transcript": text})
    except NoTranscriptFound:
        return jsonify({"error": "No transcript found for this video"}), 404
    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
