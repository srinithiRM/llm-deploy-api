from flask import Flask, request, jsonify
import os
import base64

app = Flask(__name__)

SECRET = "srinithi"  # Your secret

@app.route('/api', methods=['POST'])
def handle_request():
    data = request.get_json()
    
    # 1️⃣ Verify secret
    if not data or data.get("secret") != SECRET:
        return jsonify({"error": "Invalid secret"}), 403
    
    # 2️⃣ Parse basic fields
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
    
    # 4️⃣ Create a minimal HTML app file
    app_filename = f"{task}_index.html"
    with open(app_filename, "w") as f:
        f.write(f"""
<!doctype html>
<html>
<head><title>{task}</title></head>
<body>
<h1>{brief}</h1>
</body>
</html>
""")
    
    # 5️⃣ Prepare JSON response
    response = {
        "status": "ok",
        "message": f"Task {task} received from {email}",
        "round": round_index,
        "nonce": nonce,
        "html_file": app_filename
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


