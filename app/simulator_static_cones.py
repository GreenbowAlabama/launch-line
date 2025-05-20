# simulator_static_cones.py

import os
import cv2
import argparse
import time
import numpy as np
import subprocess
from app.detector import BallDetector
from app.tracker import BallTracker
from app.visualizer import draw_overlay
from app.logger import KickLogger
from app.utils import load_lab_config

RESET_AFTER_SECONDS = 3
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

def run_simulator(source, is_rtsp):
    # Load video source
    if is_rtsp:
        ffmpeg_cmd = [
            'ffmpeg', '-rtsp_transport', 'tcp', '-i', source,
            '-vf', f'scale={FRAME_WIDTH}:{FRAME_HEIGHT}',
            '-preset', 'ultrafast', '-fflags', 'nobuffer', '-flags', 'low_delay',
            '-f', 'image2pipe', '-pix_fmt', 'bgr24', '-vcodec', 'rawvideo', '-an', '-sn', '-'
        ]
        pipe = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, bufsize=10**8)
        fps = 30  # Default fallback
    else:
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video file: {source}")
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Video FPS detected: {fps:.2f}")

    # Load lab config
    config = load_lab_config()
    print(f"[CONFIG] Loaded: {config}")

    # Set up core components
    detector = BallDetector()
    tracker = BallTracker(
        cone_distance_ft=config['cones']['cone2_offset_ft'] - config['cones']['cone1_offset_ft'],
        mph_conversion=0.681818,
        fps=fps
    )
    logger = KickLogger()

    # Hardcoded cone line coordinates (for overlay purposes)
    tracker.set_static_cones(
        cone1_start=(281, 297),
        cone1_end=(886, 453),
        cone2_start=(330, 271),
        cone2_end=(886, 368),
        frame_width=1280,
        frame_height=720
    )

    result_text = ""
    last_result_time = 0
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

        overlay = frame.copy()
        status_message = "Tracking..."
        detections = detector.detect(frame)

        center_x = center_y = None
        best_conf = 0.0

        if detections:
            print(f"Frame {frame_count}: {len(detections)} detections")

        for det in detections:
            x1, y1, x2, y2 = map(int, det[:4])
            conf = float(det[4])
            # print(f" - Detection box: ({x1}, {y1}) to ({x2}, {y2}), conf={conf:.2f}")

            if conf > best_conf:
                best_conf = conf
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                print(f" - Detection box: ({x1}, {y1}) to ({x2}, {y2}), conf={conf:.2f}")

            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 100, 255), 2)
            cv2.putText(overlay, f"{conf:.2f}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 255), 1)

        if best_conf > 0:
            status_message = f"Ball detected (conf {best_conf:.2f})"

        if center_x is not None:
            status_message, result = tracker.update(center_x, center_y, frame_count)
            if result:
                result_text = status_message
                logger.log(result, result['result'])
                last_result_time = time.time()

        if result_text and (time.time() - last_result_time > RESET_AFTER_SECONDS):
            result_text = ""

        overlay = draw_overlay(frame, tracker, result_text, status_message, FRAME_WIDTH, FRAME_HEIGHT)
        cv2.imshow("Launch Monitor Simulator", overlay)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    logger.close()
    if not is_rtsp:
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["live", "replay"], default="live")
    parser.add_argument("--source", required=False, help="RTSP URL or video file path")
    args = parser.parse_args()

    source = args.source or os.getenv("RTSP_URL")
    if not source:
        raise ValueError("Source must be provided via --source or RTSP_URL environment variable")

    is_rtsp = args.mode == "live"
    run_simulator(source, is_rtsp)