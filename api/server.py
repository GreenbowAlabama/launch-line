import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from api.auth import auth_bp
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET", "secret")
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB

# Allow CORS for all /auth/* routes (adjust origins if needed later)
CORS(app, resources={r"/auth/*": {"origins": "*"}})

# Register authentication routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")

# Health check endpoint
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route("/api/simulate", methods=["POST"])
def simulate():
    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video_file = request.files["video"]
    if video_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(video_file.filename)
    save_path = os.path.join("/tmp", filename)
    video_file.save(save_path)

    # Placeholder logic – replace with actual ball tracking logic
    result = {
        "speed_mph": 42.0,
        "result_text": "Goal!",
    }

    # Optionally delete the file after processing
    os.remove(save_path)

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)