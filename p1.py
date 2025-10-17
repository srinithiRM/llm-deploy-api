from flask import Flask, request, jsonify
import os
import requests
# from builder import generate_and_deploy_app  # (you’ll add this later)

app = Flask(__name__)

SECRET = "srinithi"

@app.route("/api", methods=["POST"])
def handle_request():
    data = request.get_json()
    if not data or data.get("secret") != SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    # Immediate acknowledgment
    response = {"status": "ok", "message": "Request received"}
    print("Received:", data)

    # TODO: Build + deploy logic (background or inline)
    # generate_and_deploy_app(data)

    return jsonify(response), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

