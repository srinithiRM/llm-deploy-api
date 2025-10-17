from flask import Flask, request, jsonify
import os
import base64
import subprocess
import datetime

app = Flask(__name__)

# Your secret for verifying requests
SECRET = "srinithi"

# GitHub repo and token
GITHUB_REPO = "https://github.com/srinithiRM/llm-deploy-api.git"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # Recommended to set this as an environment variable

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

    # 3️⃣ Save attachments
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

    # 4️⃣ Generate a minimal HTML app
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

    # 5️⃣ Push to GitHub
    try:
        subprocess.run(["git", "checkout", "main"], check=True)
        subprocess.run(["git", "add", app_filename] + saved_files, check=True)
        commit_msg = f"Add task {task} by {email} at {datetime.datetime.now().isoformat()}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        # Use token in URL for authentication
        repo_with_token = GITHUB_REPO.replace("https://", f"https://{GITHUB_TOKEN}@")
        subprocess.run(["git", "push", repo_with_token, "main"], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Git push failed", "details": str(e)}), 500

    # 6️⃣ Prepare response
    response = {
        "status": "ok",
        "message": f"Task {task} received from {email}",
        "round": round_index,
        "nonce": nonce,
        "app_file": app_filename
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


