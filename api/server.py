# api/server.py

import os
from flask import Flask, jsonify
from flask_cors import CORS
from api.auth import auth_bp

app = Flask(__name__)
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET", "secret")
CORS(app, resources={r"/auth/*": {"origins": "*"}}) 

# Register authentication routes (only once)
app.register_blueprint(auth_bp, url_prefix="/auth")

# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)