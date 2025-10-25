import os
from pathlib import Path
import shutil


def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def save_upload_file(upload_file_stream, dst_path: str):
    """
    upload_file_stream: file-like object (stream)
    dst_path: target full path
    """
    ensure_dir(os.path.dirname(dst_path))
    with open(dst_path, "wb") as f:
        shutil.copyfileobj(upload_file_stream, f)
    return dst_path


def make_output_path(input_path: str, output_dir: str, suffix="_skeleton.mp4"):
    base = Path(input_path).stem
    return str(Path(output_dir) / f"{base}{suffix}")