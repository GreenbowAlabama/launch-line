# app.py

from flask import Flask, render_template_string, jsonify

MEDIA_SERVER = "http://4.255.67.198:8888"

app = Flask(__name__)

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
        "camera": "pending",
        "fps": None,
        "message": "App is running and waiting for RTSP stream"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
