from flask import Flask, request, send_file
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2>YouTube Clip Downloader</h2>
    <form method="post" action="/download">
        <input name="url" placeholder="YouTube URL" required><br><br>
        <input name="start" placeholder="Start time (MM:SS)" required><br><br>
        <input name="end" placeholder="End time (MM:SS)" required><br><br>
        <button type="submit">Download Clip</button>
    </form>
    """

@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]
    start = request.form["start"]
    end = request.form["end"]

    uid = uuid.uuid4().hex
    temp = f"temp_{uid}.mp4"
    out = f"clip_{uid}.mp4"

    subprocess.run(
        ["yt-dlp", "-f", "bv*+ba/b", "-o", temp, url],
        check=True
    )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss", start,
            "-to", end,
            "-i", temp,
            "-c:v", "libx264",
            "-c:a", "aac",
            out
        ],
        check=True
    )

    os.remove(temp)
    return send_file(out, as_attachment=True)

if __name__ == "__main__":
   if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


