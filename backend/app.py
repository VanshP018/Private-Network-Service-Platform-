"""
Minimal REST backend for the Computer Networks course project.
Run the SAME file on Mac 3 (BACKEND_ID=A, PORT=3001) and
Mac 4 (BACKEND_ID=B, PORT=3002).

Usage:
    BACKEND_ID=A PORT=3001 python3 app.py
"""
from flask import Flask, jsonify, make_response
import os
import socket

app = Flask(__name__)
BACKEND_ID = os.environ.get("BACKEND_ID", "A")
PORT = int(os.environ.get("PORT", 3001))


@app.route("/")
def home():
    return jsonify(
        message=f"Backend {BACKEND_ID} is running",
        hostname=socket.gethostname(),
    )


@app.route("/api/status")
def status():
    resp = make_response(jsonify(backend=BACKEND_ID, status="ok", hostname=socket.gethostname()))
    resp.headers["X-Backend"] = BACKEND_ID
    resp.headers["Cache-Control"] = "max-age=60"
    return resp


if __name__ == "__main__":
    # host=0.0.0.0 is required so OTHER Macs on the LAN can reach this service.
    # Never change this to 127.0.0.1 - that would only accept connections from
    # this same machine, and nginx on Mac 2 would not be able to reach it.
    print(f"Backend {BACKEND_ID} starting on 0.0.0.0:{PORT}")
    app.run(host="0.0.0.0", port=PORT)
