from flask import Flask, request, render_template_string
import os
import subprocess
import signal
import threading

app = Flask(__name__)

MEDIA_SERVER = os.getenv("MEDIA_SERVER", "http://172.212.69.76:8888")
YOLO_PROCESS = None
YOLO_LOCK = threading.Lock()


@app.route("/")
def index():
    return render_template_string(f"""
    <html>
    <head>
        <title>Launch Labs Stream</title>
    </head>
    <body>
        <h1>Live Stream</h1>
        <video width="640" height="360" controls autoplay muted>
            <source src="{MEDIA_SERVER}/live/stream/index.m3u8" type="application/x-mpegURL">
            Your browser does not support the video tag.
        </video>
        <br/><br/>
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
    if yolo_process is None or yolo_process.poll() is not None:
        yolo_process = subprocess.Popen(["python3", YOLO_SCRIPT])
        return "Started YOLO detection process.", 200
    return "Detection already running.", 200


@app.route("/stop", methods=["POST"])
def stop_detection():
    global yolo_process
    if yolo_process and yolo_process.poll() is None:
        yolo_process.terminate()
        yolo_process.wait()
        yolo_process = None
        return "Stopped YOLO detection process.", 200
    return "No detection process running.", 200


@app.route("/healthz")
def health():
    return "ok", 200


@app.route("/status")
def status():
    return {
        "status": "running" if yolo_process and yolo_process.poll() is None else "idle",
        "rtsp_url": os.getenv("RTSP_STREAM_URL", "unset")
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
