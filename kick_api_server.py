from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

last_kick_result = None

@app.route("/api/push", methods=["POST"])
def push_kick_result():
    global last_kick_result
    last_kick_result = request.json
    print("[UI] Kick result received:", last_kick_result)
    return jsonify({"status": "ok"})

@app.route("/api/latest", methods=["GET"])
def get_latest_result():
    if last_kick_result:
        return jsonify(last_kick_result)
    else:
        return jsonify({"status": "waiting"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)