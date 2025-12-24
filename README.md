# Dance Movement Analysis — Flask + MediaPipe

## Overview
Dance Movement Analysis is a Flask-based web service that allows users to upload short dance videos, detects human body keypoints using MediaPipe, and returns a processed video with skeleton overlays. It is ideal for dance instructors, choreographers, and anyone interested in analyzing dance movements for learning, training, or performance improvement.

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

│   ├── app2.py                 # Main Flask application

│   ├── movement_analysis.py   # Video processing and skeleton overlay logic

│   ├── movement_analysis2.py   

│   ├── utils.py               # Utility functions (file handling, paths)

├── config/

│   └── settings.py            # Project configuration and environment variables

├── temp/

│   └── a1.wav

│   └── a2.wav

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

### 3. Install dependencies
pip install --upgrade pip setuptools wheel

pip install -r requirements.txt

### 4. Run the Flask server
python -m app.app
### The server will start at:
http://127.0.0.1:5000

<<<<<<< HEAD
### stop it (Ctrl + C) after executing locally

### 5. Docker Setup (Windows Local Test)
### 5.1 Build Docker image
docker build -t dance-analyzer .

### 5.2 Run Docker container
docker run -p 5000:5000 dance-analyzer
### alternate command to run the Docker container
docker run dance-analyzer (simplier to execute)

### 6. Test upload and processing
### Use the /analyze endpoint to upload a video via POST request.
curl -X POST \
     -F "file=@app/sample_videos/sample_dance.mp4" \
     http://localhost:5000/analyze --output result.mp4


### 7. Cloud Deployment (Ubuntu on AWS)
=======
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
>>>>>>> d090c04 (second commit)
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
<<<<<<< HEAD
=======
### rerun the docker image build command after this
>>>>>>> d090c04 (second commit)

### rerun the docker image build command after this

### 7.6 Run container
sudo docker run -d -p 5000:5000 dance-analyzer

<<<<<<< HEAD
=======
### 7.6 Run container on cloud
sudo docker run -d -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  dance-analyzer
>>>>>>> d090c04 (second commit)
(or) alternate one

docker run -p 5000:5000 dance-analyzer # (recommended)

### 8. AWS EC2 Deployment
### 8.1 Connect to EC2 Instance (Ubuntu)
After downloading your .pem key:
### use these commands:
chmod 400 dance-server.pem

ssh -i "dance-server.pem" ubuntu@<EC2-PUBLIC-IP>

### 8.2 Update System
sudo apt update && sudo apt upgrade -y

### 8.3 Install Docker and curl in Ubuntu
sudo apt install docker.io -y

sudo apt install -y curl

sudo systemctl start docker

sudo systemctl enable docker

### verify the version of the docker
docker --version

### Install Git
sudo apt install git -y

### 8.4 Clone Your Project Inside EC2
git clone https://github.com/Vamshi052004/Cloud-based-Dance-Movement-Analysis-Server.git

cd Cloud-based-Dance-Movement-Analysis-Server

### 8.5 Upload Sample Video (from your laptop to EC2)
scp -i "dance-server.pem" sample_dance.mp4 ubuntu@(EC2-PUBLIC-IP):~/Cloud-based-Dance-Movement-Analysis-Server/

### 8.6 Build Docker Image
sudo docker build -t dance-analyzer .

### 8.7 Run Docker Container
sudo docker run -d -p 5000:5000 dance-analyzer

(or)

sudo docker run -p 5000:5000 dance-analyzer

### 9. Test API on EC2 (POST Method)
curl -X POST http://<EC2-IP>:5000/analyze \
  -F "file=@sample_videos/sample_dance.mp4" \
  --output result.mp4

### Testing
### Unit tests are provided for video analysis and API endpoints.
python -m pytest -v


<<<<<<< HEAD

### References
=======


MediaPipe Pose -> https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker

Flask Documentation -> https://flask.palletsprojects.com/en/stable/

OpenCV Documentation -> https://docs.opencv.org/4.x/

