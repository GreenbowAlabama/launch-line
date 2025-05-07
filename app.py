from flask import Flask, render_template_string, request, jsonify
import os
import subprocess
import threading
import signal

app = Flask(__name__)

MEDIA_SERVER = os.getenv("MEDIA_SERVER", "http://172.212.69.76:8888")
RTSP_STREAM_URL = os.getenv("RTSP_STREAM_URL", "rtsp://172.212.69.76:8554/live/stream")

yolo_process = None
yolo_lock = threading.Lock()


@app.route("/")
def index():
    return render_template_string(f"""
        <html>
        <head>
            <title>Launch Labs Stream</title>
        </head>
        <body>
            <h1>Live Stream</h1>
            <video width="640" height="360" controls autoplay>
                <source src="{MEDIA_SERVER}/live/stream/index.m3u8" type="application/x-mpegURL">
                Your browser does not support the video tag.
            </video>
            <br><br>
            <form action="/start" method="post">
                <button type="submit">Start Detection</button>
            </form>
            <form action="/stop" method="post">
                <button type="submit">Stop Detection</button>
            </form>
        </body>
        </html>
    """)


@app.route("/start", methods=["POST"])
def start_detection():
    global yolo_process
    with yolo_lock:
        if yolo_process is None or yolo_process.poll() is not None:
            print("Starting YOLO detection process...")
            yolo_process = subprocess.Popen(["python3", "yolo_main_with_goal.py"])
    return "Detection started", 200


@app.route("/stop", methods=["POST"])
def stop_detection():
    global yolo_process
    with yolo_lock:
        if yolo_process and yolo_process.poll() is None:
            print("Stopping YOLO detection process...")
            yolo_process.terminate()
            yolo_process.wait()
            yolo_process = None
    return "Detection stopped", 200


@app.route("/healthz")
def health():
    return "ok", 200


@app.route("/status")
def status():
    return jsonify({
        "status": "running" if yolo_process and yolo_process.poll() is None else "idle",
        "camera": "pending",
        "fps": None,
        "message": "App is running and waiting for RTSP stream"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)