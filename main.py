import os
import threading
import time

from flask import Flask, render_template, request, send_file

from pytube import YouTube

from moviepy.editor import AudioFileClip


app = Flask(__name__)


# convert mp4 to mp3
def convert_mp4_to_mp3(mp4_file_path, mp3_file_path):
    audio = AudioFileClip(mp4_file_path)
    audio.write_audiofile(mp3_file_path)


# delete file after delay
def delete_file_after_delay(filename, delay):
    time.sleep(delay)
    if os.path.exists(filename):
        os.remove(filename)


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return render_template('index.html', name=name)

@app.route("/download", methods=["POST"])
def download_video():
    url = request.form.get("url")
    yt = YouTube(url)
    if yt is None:
        return "Error: Invalid URL or video does not exist"
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if video is None:
        return "Error: No suitable stream found"
    filename = video.default_filename
    video.download(filename=filename)
    mp3_filename = filename.rsplit('.', 1)[0] + '.mp3'  # replace .mp4 with .mp3
    convert_mp4_to_mp3(filename, mp3_filename)
    # Schedule file deletion in 30 minutes (1800 seconds)
    threading.Thread(target=delete_file_after_delay, args=(filename, 900)).start()
    return render_template('download.html', filename=mp3_filename)

@app.route("/video/<filename>")
def serve_video(filename):
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))