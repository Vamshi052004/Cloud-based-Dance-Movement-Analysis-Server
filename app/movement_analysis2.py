import cv2
import mediapipe as mp
import numpy as np
import librosa
import subprocess
import os

FFMPEG_PATH = r"C:\\Users\\K VAMSHIDHAR REDDY\\ffmpeg\bin\\ffmpeg.exe"

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

def extract_audio(video_path, audio_path):
    subprocess.run([
        FFMPEG_PATH, "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "22050",
        audio_path
    ], check=True)

def first_beat_time(audio_path):
    y, sr = librosa.load(audio_path, sr=22050)
    _, beats = librosa.beat.beat_track(y=y, sr=sr)
    times = librosa.frames_to_time(beats, sr=sr)
    return times[0] if len(times) else 0.0

def sync_video(video, offset, output):
    if offset >= 0:
        subprocess.run([
            FFMPEG_PATH, "-y",
            "-itsoffset", str(offset),
            "-i", video,
            "-map", "0:v",
            "-map", "0:a?",
            "-c", "copy",
            output
        ], check=True)
    else:
        subprocess.run([
            FFMPEG_PATH, "-y",
            "-i", video,
            "-ss", str(abs(offset)),
            "-c", "copy",
            output
        ], check=True)

def pose_similarity(lm1, lm2):
    if lm1 is None or lm2 is None:
        return 0.0

    p1 = np.array([[p.x, p.y] for p in lm1.landmark])
    p2 = np.array([[p.x, p.y] for p in lm2.landmark])
    dist = np.linalg.norm(p1 - p2, axis=1).mean()
    return (1 / (1 + dist)) * 100

def merge_and_analyze(video1, video2, output_path):
    cap1 = cv2.VideoCapture(video1)
    cap2 = cv2.VideoCapture(video2)

    fps = int(min(
        cap1.get(cv2.CAP_PROP_FPS),
        cap2.get(cv2.CAP_PROP_FPS)
    )) or 25

    w1, h1 = int(cap1.get(3)), int(cap1.get(4))
    w2, h2 = int(cap2.get(3)), int(cap2.get(4))

    height = min(h1, h2)
    width = w1 + w2

    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    frames = 0

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:

        while True:
            r1, f1 = cap1.read()
            r2, f2 = cap2.read()
            if not r1 or not r2:
                break

            f1 = cv2.resize(f1, (w1, height))
            f2 = cv2.resize(f2, (w2, height))

            p1 = pose.process(cv2.cvtColor(f1, cv2.COLOR_BGR2RGB))
            p2 = pose.process(cv2.cvtColor(f2, cv2.COLOR_BGR2RGB))

            if p1.pose_landmarks:
                mp_draw.draw_landmarks(f1, p1.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            if p2.pose_landmarks:
                mp_draw.draw_landmarks(f2, p2.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            sim = pose_similarity(p1.pose_landmarks, p2.pose_landmarks)

            cv2.putText(f1, "Video 1", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.putText(f2, f"Similarity: {sim:.2f}%", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            merged = np.hstack((f1, f2))
            out.write(merged)
            frames += 1

    cap1.release()
    cap2.release()
    out.release()

    return fps, frames

def process_two_videos(video1, video2, final_output):
    os.makedirs("temp", exist_ok=True)

    a1, a2 = "temp/a1.wav", "temp/a2.wav"
    extract_audio(video1, a1)
    extract_audio(video2, a2)

    offset = first_beat_time(a2) - first_beat_time(a1)

    v1_sync = "temp/v1_sync.mp4"
    v2_sync = "temp/v2_sync.mp4"

    sync_video(video1, 0, v1_sync)
    sync_video(video2, offset, v2_sync)

    merge_and_analyze(v1_sync, v2_sync, final_output)
