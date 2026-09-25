import eventlet
eventlet.monkey_patch()

import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_socketio import SocketIO

load_dotenv()

app = Flask(__name__)

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")

socketio = SocketIO(
    app,
    cors_allowed_origins=ALLOWED_ORIGINS,
    async_mode="eventlet",
    message_queue=REDIS_URL,
)


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))