import os
import subprocess
import signal
import threading
from flask import Flask, render_template_string, request

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.dev")

app = Flask(__name__)

MEDIA_SERVER = os.getenv("MEDIA_SERVER")
YOLO_PROCESS = None
YOLO_LOCK = threading.Lock()


@app.route("/")
def index():
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Launch Labs Demo</title>
        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    </head>
    <body>
        <h1>Launch Labs Demo</h1>
        <video id="video" width="640" height="360" controls autoplay muted></video>
        <br><br>
        <button onclick="startDetection()">Start Detection</button>
        <button onclick="stopDetection()">Stop Detection</button>

        <script>
            function startDetection() {{
                fetch('/start', {{ method: 'POST' }});
            }}

            function stopDetection() {{
                fetch('/stop', {{ method: 'POST' }});
            }}

            document.addEventListener("DOMContentLoaded", function () {{
                var video = document.getElementById("video");
                var videoSrc = "{MEDIA_SERVER}/stream/index.m3u8";
                if (Hls.isSupported()) {{
                    var hls = new Hls();
                    hls.loadSource(videoSrc);
                    hls.attachMedia(video);
                    hls.on(Hls.Events.MANIFEST_PARSED, function () {{
                        video.play();
                    }});
                }} else if (video.canPlayType("application/vnd.apple.mpegurl")) {{
                    video.src = videoSrc;
                    video.addEventListener("loadedmetadata", function () {{
                        video.play();
                    }});
                }}
            }});
        </script>
    </body>
    </html>
    """)


@app.route("/start", methods=["POST"])
def start_detection():
    global YOLO_PROCESS
    with YOLO_LOCK:
        if YOLO_PROCESS is None or YOLO_PROCESS.poll() is not None:
            YOLO_PROCESS = subprocess.Popen(["python3", "yolo_main.py"])
    return "", 200


@app.route("/stop", methods=["POST"])
def stop_detection():
    global YOLO_PROCESS
    with YOLO_LOCK:
        if YOLO_PROCESS is not None and YOLO_PROCESS.poll() is None:
            YOLO_PROCESS.terminate()
            YOLO_PROCESS.wait()
            YOLO_PROCESS = None
    return "", 200


if __name__ == "__main__":
    print("Loading .env.dev...")
    print("Starting Flask app...")
    app.run(host="0.0.0.0", port=80)