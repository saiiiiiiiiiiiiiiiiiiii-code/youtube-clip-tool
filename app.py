from flask import Flask, request, send_file
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2>Video Clip Tool</h2>
    <p>Upload a video and download a clipped segment.</p>
    <form method="post" action="/clip" enctype="multipart/form-data">
        <input type="file" name="video" required><br><br>
        <input name="start" placeholder="Start time (MM:SS)" required><br><br>
        <input name="end" placeholder="End time (MM:SS)" required><br><br>
        <button type="submit"
                onclick="this.innerText='Processing... please wait';">
            Clip Video
        </button>
    </form>
    <p><small>Note: Free server, processing may take a few seconds.</small></p>
    """

@app.route("/clip", methods=["POST"])
def clip():
    try:
        video = request.files["video"]
        start = request.form["start"]
        end = request.form["end"]

        uid = uuid.uuid4().hex
        input_file = f"input_{uid}.mp4"
        output_file = f"clip_{uid}.mp4"

        video.save(input_file)

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss", start,
                "-to", end,
                "-i", input_file,
                "-c:v", "libx264",
                "-c:a", "aac",
                output_file
            ],
            check=True
        )

        os.remove(input_file)
        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return f"<h3>Error</h3><pre>{str(e)}</pre>", 500

