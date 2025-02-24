from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

# Directory to store temporary files
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ✅ Add this function to show a message on the home page
@app.route('/')
def home():
    return "Welcome to the YouTube to MP3 API! Use the /download endpoint."

def download_mp3(url):
    """Downloads and converts YouTube video to MP3."""
    unique_id = str(uuid.uuid4())
    filename = os.path.join(DOWNLOAD_FOLDER, unique_id)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{filename}.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            mp3_filename = f"{filename}.mp3"
            return mp3_filename, info['title']
    except Exception as e:
        return None, str(e)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    mp3_file, title = download_mp3(url)
    if mp3_file:
        return send_file(mp3_file, as_attachment=True)
    else:
        return jsonify({"error": title}), 500

if __name__ == "__main__":
    app.run(debug=True)
