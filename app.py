# app.py
import subprocess
import os
import signal
from flask import Flask, render_template_string, jsonify

MEDIA_SERVER = os.getenv("MEDIA_SERVER", "http://172.212.69.76:8888")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string(f"""
        <html>
        <head>
            <title>Launch Labs Stream</title>
            <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
        </head>
        <body>
            <h1>Live Stream</h1>
            <video id="video" width="640" height="360" controls autoplay muted></video>
            <script>
                const video = document.getElementById('video');
                const hlsSource = '{MEDIA_SERVER}/live/stream/index.m3u8';
                if (Hls.isSupported()) {{
                    const hls = new Hls();
                    hls.loadSource(hlsSource);
                    hls.attachMedia(video);
                }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
                    video.src = hlsSource;
                }} else {{
                    console.error("This browser does not support HLS.");
                }}
            </script>
        </body>
        </html>
    """)

@app.route("/healthz")
def health():
    return "ok", 200

@app.route("/status")
def status():
    return jsonify({
        "status": "idle",
        "camera": "streaming",
        "fps": None,
        "message": "Connected to live HLS stream"
    })

if __name__ == "__main__":
    yolo_process = subprocess.Popen(["python3", "yolo_main_with_goal.py"])
    try:
        app.run(host="0.0.0.0", port=80)
    finally:
        os.kill(yolo_process.pid, signal.SIGTERM)