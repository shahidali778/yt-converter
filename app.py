import os
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

# Folder to save downloads
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_audio(url):
    """Downloads YouTube audio in M4A format (closest to MP3, no FFmpeg)."""
    options = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'postprocessors': [],  # No FFmpeg needed
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)

    return filename  # Returns downloaded file path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", error="Please enter a valid URL.")

        try:
            filepath = download_audio(url)
            return render_template("index.html", filepath=filepath, filename=os.path.basename(filepath))
        except Exception as e:
            return render_template("index.html", error=f"Download failed: {str(e)}")

    return render_template("index.html")

@app.route("/download/<filename>")
def download(filename):
    """Serve the file for download."""
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
