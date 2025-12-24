import os
from pathlib import Path
from uuid import uuid4
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import settings
from app.utils import ensure_dir, save_upload_file, make_output_path
from app.movement_analysis import analyze_video_with_skeleton

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = settings.UPLOAD_DIR
OUTPUT_DIR = settings.OUTPUT_DIR
ensure_dir(UPLOAD_DIR)
ensure_dir(OUTPUT_DIR)


@app.route("/", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Dance Movement Analysis Flask Server Running"})


@app.route("/analyze", methods=["POST"])
def analyze():
    """Upload and analyze a video file."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    ext = Path(file.filename).suffix.lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        return jsonify({"error": f"Unsupported file type: {ext}"}), 400

    uid = uuid4().hex
    saved_name = f"{uid}_{file.filename}"
    input_path = os.path.join(UPLOAD_DIR, saved_name)

    try:
        save_upload_file(file.stream, input_path)
    except Exception as e:
        return jsonify({"error": f"Failed to save upload: {e}"}), 500

    output_path = make_output_path(input_path, OUTPUT_DIR)

    try:
        out_file, frames = analyze_video_with_skeleton(input_path, output_path)
    except Exception as e:
        try:
            os.remove(input_path)
        except Exception:
            pass
        return jsonify({"error": f"Analysis failed: {e}"}), 500

    try:
        os.remove(input_path)
    except Exception:
        pass

    return jsonify({
        "message": "Analysis complete",
        "output_video": Path(out_file).name,
        "frames_processed": frames,
        "download_url": f"/download/{Path(out_file).name}"
    })


@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    """Download processed video."""
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
