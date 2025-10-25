import os
from pathlib import Path
import pytest
from app.movement_analysis import analyze_video_with_skeleton
from config import settings

SAMPLE_VIDEO = Path(__file__).parent.parent / "app" / "sample_videos" / "sample_dance.mp4"

@pytest.mark.skipif(not SAMPLE_VIDEO.exists(), reason="Sample video not present")
def test_analyze_video_creates_output():
    out_dir = Path(settings.OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "test_output.mp4"
    out_file, frames = analyze_video_with_skeleton(str(SAMPLE_VIDEO), str(output_path))
    assert Path(out_file).exists()
    assert frames > 0
    # cleanup
    Path(out_file).unlink(missing_ok=True)