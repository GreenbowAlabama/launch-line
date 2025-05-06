# app.py
import os
import signal
import subprocess
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)
MEDIA_SERVER = "http://4.255.67.198:8888"
yolo_process = None

@app.route("/")
def index():
    return render_template_string(f"""
    <html>
    <head><title>Launch Labs Stream</title></head>
    <body>
        <h1>Live Stream</h1>
        <video width="640" height="360" controls autoplay>
            <source src="{MEDIA_SERVER}/live/stream/index.m3u8" type="application/x-mpegURL">
            Your browser does not support the video tag.
        </video>
        <br/>
        <form method="POST" action="/start">
            <button type="submit">Start Detection</button>
        </form>
        <form method="POST" action="/stop">
            <button type="submit">Stop Detection</button>
        </form>
    </body>
    </html>
    """)

@app.route("/healthz")
def health():
    return "ok", 200

@app.route("/status")
def status():
    return jsonify({
        "status": "running" if yolo_process and yolo_process.poll() is None else "idle"
    })

@app.route("/start", methods=["POST"])
def start_detection():
    global yolo_process
    if yolo_process is None or yolo_process.poll() is not None:
        yolo_process = subprocess.Popen(["python3", "yolo_main_with_goal.py"])
        return "Detection started", 200
    return "Detection already running", 200

@app.route("/stop", methods=["POST"])
def stop_detection():
    global yolo_process
    if yolo_process and yolo_process.poll() is None:
        os.kill(yolo_process.pid, signal.SIGTERM)
        yolo_process = None
        return "Detection stopped", 200
    return "No detection process to stop", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)