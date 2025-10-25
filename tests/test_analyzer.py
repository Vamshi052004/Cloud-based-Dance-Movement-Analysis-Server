import io
from pathlib import Path
import pytest
from app.app import app
from config import settings

SAMPLE_VIDEO = Path(__file__).parent.parent / "app" / "sample_videos" / "sample_dance.mp4"

@pytest.mark.skipif(not SAMPLE_VIDEO.exists(), reason="Sample video not present")
def test_analyze_endpoint_and_download(tmp_path):
    client = app.test_client()
    with open(SAMPLE_VIDEO, "rb") as f:
        data = {
            "file": (io.BytesIO(f.read()), "sample_dance.mp4")
        }
        resp = client.post("/analyze", content_type="multipart/form-data", data=data)
    assert resp.status_code == 200
    j = resp.get_json()
    assert "output_video" in j
    # try download
    dl = client.get(j["download_url"])
    assert dl.status_code == 200