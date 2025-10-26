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
├── app/
│   ├── __init__.py
│   ├── app.py                 # Main Flask application
│   ├── movement_analysis.py   # Video processing and skeleton overlay logic
│   ├── utils.py               # Utility functions (file handling, paths)
│   └── sample_videos/
│       └── sample_dance.mp4   # Sample videos for testing
├── config/
│   └── settings.py            # Project configuration and environment variables
├── demo/
│   └── demo.mp4               # Demo video of 2 minutes
├── tests/
│   ├── test_analyzer.py       # Unit tests for analyzer
│   └── test_movement.py       # Unit tests for movement analysis
├── requirements.txt           # Python package dependencies
├── Dockerfile                 # Docker setup for containerized deployment
├── .gitignore                 # Ignored files and directories
└── README.md                  # Project documentation

## Quick Start (Local Setup)

### 1. Clone the repository
git clone https://github.com/Vamshi052004/Cloud-based-Dance-Movement-Analysis-Server.git
cd dance-movement-analysis

### 2. Set up a Python virtual environment (optional)
python -m venv .venv
### Activate the environment
.venv\Scripts\activate 

### Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

### 4. Run the Flask server
python -m app.app
### The server will start at:
http://127.0.0.1:5000

### 5. Test upload and processing
### Use the /analyze endpoint to upload a video via POST request.
curl -F "file=@app/sample_videos/sample_dance.mp4" http://localhost:5000/analyze

### 6. Docker Setup (Windows Local Test)
### 6.1 Build Docker image
docker build -t dance-analyzer .

### 6.2 Run Docker container
docker run -p 5000:5000 `
-v ${PWD}/uploads:/app/uploads `
-v ${PWD}/outputs:/app/outputs `
  dance-analyzer
### alternate command to run the Docker container (recommended)
docker run dance-analyzer (simplier to execute)

### 7. Cloud Deployment (Ubuntu on AWS / GCP)
### 7.1 Update system and install Docker
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

### 7.2 check the docker version
docker --version

### 7.3 Clone/copy the repository from the github
git clone https://github.com/Vamshi052004/Cloud-based-Dance-Movement-Analysis-Server.git

### 7.4 Build Docker image on Ubuntu
cd dance-movement-analysis
sudo docker build -t dance-analyzer .

### 7.5 If any issue occur while building the docker image (Optional if no issues occured)
df -h
sudo docker system prune -a
sudo docker system df
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*
sudo journalctl --vacuum-time=1d
### rerun the docker image build command after this


### 7.6 Run container on cloud
sudo docker run -d -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  dance-analyzer
(or) alternate one
docker run -p 5000:5000 dance-analyzer # (recommended)

### Install curl in Ubuntu
sudo apt update
sudo apt install -y curl

### Access the deployed API
curl -X POST http://<EC2-IP>:5000/analyze \
  -F "file=@sample_videos/sample_dance.mp4" \
  --output result.mp4

### Testing
# Unit tests are provided for video analysis and API endpoints.
python -m pytest -v


License
This project is licensed under the MIT License. See LICENSE for details.

References
MediaPipe Pose -> https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
Flask Documentation -> https://flask.palletsprojects.com/en/stable/
OpenCV Documentation -> https://docs.opencv.org/4.x/
