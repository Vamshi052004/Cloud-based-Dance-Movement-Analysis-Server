# Dance Movement Analysis — Flask + MediaPipe

## Overview
Dance Movement Analysis is a Flask-based web service that allows users to upload short dance videos, detects human body keypoints using [MediaPipe](https://mediapipe.dev/), and returns a processed video with skeleton overlays. It is ideal for dance instructors, choreographers, and anyone interested in analyzing dance movements for learning, training, or performance improvement.

---

## Features
- Upload dance videos in common formats (MP4, AVI, MOV, etc.).
- Automatic human pose detection using MediaPipe.
- Skeleton overlay visualization on uploaded videos.
- Download processed videos for offline use.
- Lightweight, container-friendly, and easy to deploy using Docker.

---

## Project Structure
dance-movement-analysis/
│
├── app/
| |___ sample_videos/
      |__ sample_dance.mp4
│ ├── app.py # Main Flask application
│ ├── movement_analysis.py # Video processing and skeleton overlay logic
│ ├── utils.py # Utility functions (file handling, paths)
│ └── sample_videos/ # Sample videos for testing
│
├── config/
│ └── settings.py # Project configuration and environment variables
│
├── demo/
│ ├── demo.mp4 # demo video of 2 minutes
│
├── tests/ # Unit tests for endpoints and video analysis
|   |__ test_analyzer.py
|   |__ test_movement.py
├── requirements.txt # Python package dependencies
├── Dockerfile # Docker setup for containerized deployment
├── .gitignore # Ignored files and directories
└── README.md # Project documentation

yaml
Copy code

---

## Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd dance-movement-analysis

# 2. Set up a Python virtual environment
```bash
python -m venv .venv
# Activate environment
source .venv/bin/activate     # macOS/Linux
.venv\Scripts\activate        # Windows

# 3. Install dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 4. Run the Flask server
```bash
python -m app.app
The server runs by default on: http://127.0.0.1:5000.

# 5. Test upload and processing
Use the /analyze endpoint to upload videos via POST.

Response JSON includes:
```json
{
  "output_video": "processed_video.mp4",
  "download_url": "/download/processed_video.mp4"
}

# Docker Setup
1. Build Docker image
```bash
docker build -t dance-analyzer .

2. Run Docker container
```bash
docker run -p 5000:5000 \
    -v $(pwd)/data/uploads:/data/uploads \
    -v $(pwd)/data/outputs:/data/outputs \
    dance-analyzer
Port 5000 is exposed; upload and output directories are mounted for persistence.

Environment Variables
Variable	Description	Default
UPLOAD_DIR	Directory to store uploaded videos	/data/uploads
OUTPUT_DIR	Directory to store processed videos	/data/outputs

# Testing
The project includes unit tests for both the Flask endpoints and video processing functions.

Run all tests with:
```bash
pytest
or 
python -m pytest -v
Ensures that uploads, analysis, and video output work correctly.

Deployment
Suitable for deployment on VPS or cloud services (AWS EC2, GCP Compute Engine, DigitalOcean, etc.).

Ensure port 5000 is open, or configure Nginx with TLS for secure production deployment.

Docker simplifies deployment, avoids dependency conflicts, and ensures reproducibility.

Usage Example
Upload Video
```bash
curl -X POST http://127.0.0.1:5000/analyze \
  -F "file=@/path/to/sample_dance.mp4"

Response in json format
{
  "output_video": "sample_dance_processed.mp4",
  "download_url": "/download/sample_dance_processed.mp4"
}
Download Video
Open in browser or use curl:

```bash
curl -O http://127.0.0.1:5000/download/sample_dance_processed.mp4
Contributing
Fork the repository.

Create a feature branch:

bash
git checkout -b feature/my-feature
Commit changes:

bash
git commit -m "Add feature"
Push branch:

bash
git push origin feature/my-feature
Open a pull request.

License
This project is licensed under the MIT License. See LICENSE for details.

References
MediaPipe Pose -> https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
Flask Documentation -> https://flask.palletsprojects.com/en/stable/
OpenCV Documentation -> https://docs.opencv.org/4.x/