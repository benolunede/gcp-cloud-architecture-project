os import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_helsinki():
    return jsonify({
        "status": "online",
        "framework": "Flask/Python",
        "target_market": "English-only Helsinki Tech Teams",
        "message": "Cloud Infrastructure Active!"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
