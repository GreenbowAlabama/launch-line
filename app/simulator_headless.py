# simulator_headless.py

import os
import cv2
import argparse
import time
import requests
import numpy as np
import subprocess
from app.detector import BallDetector
from app.tracker import BallTracker
from app.logger import KickLogger
from app.utils import load_lab_config

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

def run_headless(source, is_rtsp):
    if is_rtsp:
        ffmpeg_cmd = [
            'ffmpeg', '-rtsp_transport', 'tcp', '-i', source,
            '-vf', f'scale={FRAME_WIDTH}:{FRAME_HEIGHT}',
            '-preset', 'ultrafast', '-fflags', 'nobuffer', '-flags', 'low_delay',
            '-f', 'image2pipe', '-pix_fmt', 'bgr24', '-vcodec', 'rawvideo', '-an', '-sn', '-'
        ]
        pipe = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, bufsize=10**8)
        fps = 30
    else:
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video file: {source}")
        fps = cap.get(cv2.CAP_PROP_FPS)

    config = load_lab_config()
    print(f"[CONFIG] Loaded: {config}")

    detector = BallDetector()
    tracker = BallTracker(
        cone_distance_ft=config['cones']['cone2_offset_ft'] - config['cones']['cone1_offset_ft'],
        mph_conversion=0.681818,
        fps=fps
    )
    logger = KickLogger()

    tracker.set_static_cones(
        cone1_start=(281, 297),
        cone1_end=(886, 453),
        cone2_start=(330, 271),
        cone2_end=(886, 368),
        frame_width=FRAME_WIDTH,
        frame_height=FRAME_HEIGHT
    )

    frame_count = 0
    while True:
        if is_rtsp:
            raw_frame = pipe.stdout.read(FRAME_WIDTH * FRAME_HEIGHT * 3)
            if len(raw_frame) != FRAME_WIDTH * FRAME_HEIGHT * 3:
                break
            frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))
        else:
            ret, frame = cap.read()
            if not ret:
                break

        detections = detector.detect(frame)

        center_x = center_y = None
        best_conf = 0.0

        for det in detections:
            x1, y1, x2, y2 = map(int, det[:4])
            conf = float(det[4])
            if conf > best_conf:
                best_conf = conf
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

        if center_x is not None:
            status_message, result = tracker.update(center_x, center_y, frame_count)
            if result:
                logger.log(result, result['result'])
                print(f"[{frame_count}] {status_message} | Speed: {result['speed_mph']:.1f} MPH")
                try:
                    res = requests.post("http://localhost:5050/kick", json=result, timeout=2)
                    print(f"[API] POST /kick status: {res.status_code}")
                except Exception as e:
                    print(f"[ERROR] Failed to post result to API: {e}")

        frame_count += 1

    logger.close()
    if not is_rtsp:
        cap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["live", "replay"], default="live")
    parser.add_argument("--source", required=False, help="RTSP URL or video file path")
    args = parser.parse_args()

    source = args.source or os.getenv("RTSP_URL")
    if not source:
        raise ValueError("Source must be provided via --source or RTSP_URL environment variable")

    is_rtsp = args.mode == "live"
    run_headless(source, is_rtsp)