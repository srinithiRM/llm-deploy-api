from flask import Flask, request, jsonify
import os
import base64

app = Flask(__name__)

# Your secret key
SECRET = "srinithi"

@app.route('/api', methods=['POST'])
def handle_request():
    data = request.get_json()

    # 1️⃣ Verify secret
    if not data or data.get("secret") != SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    # 2️⃣ Parse fields
    email = data.get("email")
    task = data.get("task")
    round_index = data.get("round")
    nonce = data.get("nonce")
    brief = data.get("brief")
    attachments = data.get("attachments", [])

    # 3️⃣ Save attachments if any
    saved_files = []
    for attach in attachments:
        name = attach.get("name")
        url = attach.get("url")
        if name and url and url.startswith("data:"):
            header, encoded = url.split(",", 1)
            filename = f"{task}_{name}"
            with open(filename, "wb") as f:
                f.write(base64.b64decode(encoded))
            saved_files.append(filename)

    # 4️⃣ Generate HTML for the task
    app_filename = f"{task}_index.html"
    with open(app_filename, "w", encoding="utf-8") as f:
        f.write(f"""<!doctype html>
<html>
<head>
    <title>{task}</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>{brief}</h1>
    <p>Task: {task}</p>
    <p>Email: {email}</p>
    <p>Round: {round_index}</p>
    <p>Nonce: {nonce}</p>
    {''.join(f'<p>Attachment saved: {file}</p>' for file in saved_files)}
</body>
</html>""")

    # 5️⃣ Prepare JSON response
    response = {
        "status": "ok",
        "message": f"Task {task} received from {email}",
        "round": round_index,
        "nonce": nonce
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


