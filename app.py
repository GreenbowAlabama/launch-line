# app.py
from flask import Flask, jsonify, Response, render_template_string
import cv2

app = Flask(__name__)

# Replace this with your actual RTSP stream URL
RTSP_URL = "rtsp://your.camera.ip.address:554/stream"

def generate_frames():
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        raise RuntimeError("Unable to open RTSP stream.")

    while True:
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame = buffer.tobytes()
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )

@app.route("/")
def index():
    return "🚀 Launch Labs API is running!"

@app.route("/healthz")
def health():
    return "ok", 200

@app.route("/status")
def status():
    return jsonify({
        "status": "idle",
        "camera": "connected" if cv2.VideoCapture(RTSP_URL).isOpened() else "offline",
        "fps": None,
        "message": "Ready for action"
    })

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/feed")
def feed():
    return render_template_string("""
        <html>
            <head>
                <title>Launch Labs Camera Feed</title>
            </head>
            <body>
                <h1>Live RTSP Feed</h1>
                <img src="{{ url_for('video_feed') }}" width="800" />
            </body>
        </html>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
