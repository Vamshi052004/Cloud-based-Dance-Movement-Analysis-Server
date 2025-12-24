FROM python:3.11-slim

# Install system deps required by OpenCV/ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsm6 libxext6 libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project
COPY . /app

# Upgrade build tools
RUN python -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create data directories
RUN mkdir -p /data/uploads /data/outputs

ENV UPLOAD_DIR=/data/uploads
ENV OUTPUT_DIR=/data/outputs
EXPOSE 5000

# Start server (module run ensures imports work)
CMD ["python", "-m", "app.app"]