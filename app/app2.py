import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from app.movement_analysis2 import process_two_videos

app = Flask(__name__)
CORS(app)

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOAD = os.path.join(BASE, "uploads")
OUTPUT = os.path.join(BASE, "outputs")

os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok",
                    "message": "Movement Analysis Service is running."})


@app.route("/analyze", methods=["POST"])
def analyze():
    if "file1" not in request.files or "file2" not in request.files:
        return jsonify({
            "error": "Upload file1 and file2"
        }), 400

    uid = os.urandom(6).hex()

    v1 = os.path.join(UPLOAD, f"{uid}_1.mp4")
    v2 = os.path.join(UPLOAD, f"{uid}_2.mp4")

    request.files["file1"].save(v1)
    request.files["file2"].save(v2)

    output = os.path.join(OUTPUT, f"final_{uid}.mp4")

    process_two_videos(v1, v2, output)

    return jsonify({
        "status": "done",
        "output_video": os.path.basename(output),
        "download_url": f"/download/{os.path.basename(output)}"
    })


@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    path = os.path.join(OUTPUT, filename)
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
    return send_file(path, as_attachment=True, mimetype="video/mp4")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
