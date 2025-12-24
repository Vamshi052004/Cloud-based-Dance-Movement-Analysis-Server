import os

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/data/outputs")

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv"}