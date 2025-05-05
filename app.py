# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "🚀 Launch Labs API is running!"

@app.route("/healthz")
def health():
    return "ok", 200

@app.route("/status")
def status():
    # You can update this to return live status from detection logic
    return jsonify({
        "status": "idle",
        "camera": "offline",
        "fps": None,
        "message": "Ready for action"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
