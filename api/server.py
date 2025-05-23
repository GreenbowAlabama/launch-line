import os
from flask import Flask, jsonify
from flask_cors import CORS
from api.auth import auth_bp  # Ensure this path matches your project layout

app = Flask(__name__)
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET", "secret")

# Allow CORS for all /auth/* routes (adjust origins if needed later)
CORS(app, resources={r"/auth/*": {"origins": "*"}})

# Register authentication routes
app.register_blueprint(auth_bp)

# Health check endpoint
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)