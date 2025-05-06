# app.py
from flask import Flask, request, Response, render_template_string, redirect, url_for
import cv2
import threading

app = Flask(__name__)
rtsp_url = ""  # Initially empty, set through the UI

lock = threading.Lock()

def generate_frames():
    global rtsp_url
    while True:
        with lock:
            url = rtsp_url
        if not url:
            break
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            break
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        cap.release()

@app.route('/', methods=['GET'])
def index():
    return render_template_string("""
        <html>
        <head><title>Launch Labs - RTSP Stream</title></head>
        <body>
            <h1>🚀 Launch Labs - RTSP Feed Config</h1>
            <form action="{{ url_for('set_rtsp') }}" method="POST">
                <label for="rtsp">Enter RTSP URL:</label><br>
                <input type="text" id="rtsp" name="rtsp_url" value="{{ rtsp_url }}" size="60"/><br><br>
                <input type="submit" value="Update Stream">
            </form>
            {% if rtsp_url %}
                <h2>Live Stream</h2>
                <img src="{{ url_for('video_feed') }}" style="max-width: 100%; height: auto;" />
            {% endif %}
        </body>
        </html>
    """, rtsp_url=rtsp_url)

@app.route('/set_rtsp', methods=['POST'])
def set_rtsp():
    global rtsp_url
    with lock:
        rtsp_url = request.form.get('rtsp_url', '').strip()
    return redirect(url_for('index'))

@app.route('/video_feed')
def video_feed():
    if not rtsp_url:
        return "RTSP URL not set", 400
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/healthz')
def health():
    return "ok", 200

@app.route('/status')
def status():
    return {
        "status": "running",
        "camera_url": rtsp_url or "not set"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
