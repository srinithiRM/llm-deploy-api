from flask import Flask, request, jsonify

app = Flask(__name__)

SECRET = "your-secret-here"  # choose your own secret

@app.route('/api', methods=['POST'])
def handle_request():
    data = request.get_json()
    if not data or data.get('secret') != SECRET:
        return jsonify({"error": "Invalid secret"}), 403
    # Example response (HTTP 200)
    return jsonify({"status": "ok", "message": "Request received"})

if __name__ == '__main__':
    app.run(port=5000)
