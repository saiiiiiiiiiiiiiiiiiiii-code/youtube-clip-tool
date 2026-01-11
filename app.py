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
        <button type="submit"
                onclick="this.innerText='Processing... please wait';">
            Download Clip
        </button>
    </form>
    <p>Note: Free server may take 30–60 seconds on first request.</p>
    """

@app.route("/download", methods=["POST"])
def download():
    try:
        url = request.form["url"]
        start = request.form["start"]
        end = request.form["end"]

        uid = uuid.uuid4().hex
        temp_file = f"temp_{uid}.mp4"
        output_file = f"clip_{uid}.mp4"

        # Download video
        subprocess.run(
            ["yt-dlp", "-f", "bv*+ba/b", "-o", temp_file, url],
            check=True,
            timeout=120
        )

        # Cut clip (safe re-encode)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss", start,
                "-to", end,
                "-i", temp_file,
                "-c:v", "libx264",
                "-c:a", "aac",
                output_file
            ],
            check=True,
            timeout=120
        )

        os.remove(temp_file)
        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return f"<h3>Error</h3><pre>{str(e)}</pre>", 500
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# IMPORTANT:
# Do NOT put app.run() here.
# Render uses gunicorn to start the app.

