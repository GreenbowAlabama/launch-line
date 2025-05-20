# simulator.py
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

CONE_DISTANCE_FT = 8.0
MPH_CONVERSION = 0.681818
FRAME_WIDTH = 720
FRAME_HEIGHT = 1280
RESET_AFTER_SECONDS = 3

def run_simulator(source, is_rtsp):
    if is_rtsp:
        ffmpeg_cmd = [
            'ffmpeg', '-rtsp_transport', 'tcp', '-i', source,
            '-vf', 'scale=720:1280',
            '-preset', 'ultrafast', '-fflags', 'nobuffer', '-flags', 'low_delay',
            '-f', 'image2pipe', '-pix_fmt', 'bgr24', '-vcodec', 'rawvideo', '-an', '-sn', '-'
        ]
        pipe = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, bufsize=10**8)
    else:
        cap = cv2.VideoCapture(source)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Video FPS detected: {fps:.2f}")

    detector = BallDetector()
    tracker = BallTracker(CONE_DISTANCE_FT, MPH_CONVERSION, fps=60)  # hardcoded to match your video

    # Set cones statically based on the test video and fixed camera setup
    tracker.cone1_y = 372
    tracker.cone2_y = 873
    tracker.default_cone1_y = 372
    tracker.default_cone2_y = 873

    logger = KickLogger()
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
        status_message = "Ready"

        detections = detector.detect(frame)
        center_x = center_y = None

        best_conf = 0
        if len(detections) > 0:
            print(f"Frame {frame_count}: {len(detections)} detections")
        for det in detections:
            x1, y1, x2, y2 = map(int, det[:4])
            conf = float(det[4])
            print(f" - Detection box: ({x1}, {y1}) to ({x2}, {y2}), conf={conf:.2f}")
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 100, 255), 2)
            cv2.putText(overlay, f"{conf:.2f}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 255), 1)

            if conf > best_conf:
                best_conf = conf
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

        if center_y is not None:
            status_message, result = tracker.update(center_y, center_x, frame_count)
            if result:
                speed = result['speed_mph']
                result_text = f"{status_message}"
                result_type = "GOAL" if "GOAL" in result_text else "MISS"
                logger.log(result, result_type)
                last_result_time = time.time()

        if result_text and time.time() - last_result_time > RESET_AFTER_SECONDS:
            result_text = ""

        overlay = draw_overlay(overlay, tracker, result_text, status_message, FRAME_WIDTH, FRAME_HEIGHT)
        cv2.imshow("Launch Monitor Simulator", overlay)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            tracker.reset_cones()
            result_text = ""

        frame_count += 1

    logger.close()
    if not is_rtsp:
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["live", "replay"], default="live")
    parser.add_argument("--source", help="RTSP URL or video file path")
    args = parser.parse_args()

    source = args.source or os.getenv("RTSP_URL")
    if not source:
        raise ValueError("Source must be provided via --source or RTSP_URL env variable")

    is_rtsp = args.mode == "live"
    run_simulator(source, is_rtsp)