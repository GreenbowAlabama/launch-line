import os
import math
import time
import cv2
import numpy as np
import subprocess
from ultralytics import YOLO
from datetime import datetime

print("Using FFmpeg-based stream reader")

# Constants
CONE_DISTANCE_FT = 8.0
MPH_CONVERSION = 0.681818
FRAME_WIDTH = 720
FRAME_HEIGHT = 1280
GOAL_DISTANCE_YARDS = 10
GOAL_WIDTH_PX = 250
GOAL_HEIGHT_PX = 100
RESET_AFTER_SECONDS = 3

# Load YOLO model
model = YOLO("yolov8n.pt")

# Get RTSP stream from environment (required)
RTSP_STREAM_URL = os.getenv("RTSP_URL")
if not RTSP_STREAM_URL:
    raise EnvironmentError("RTSP_URL environment variable is required.")

print(f"Launching FFmpeg stream reader for {RTSP_STREAM_URL}")

ffmpeg_cmd = [
    'ffmpeg',
    '-rtsp_transport', 'tcp',
    '-i', RTSP_STREAM_URL,
    '-vf', 'scale=720:1280',
    '-preset', 'ultrafast',
    '-fflags', 'nobuffer',
    '-flags', 'low_delay',
    '-f', 'image2pipe',
    '-pix_fmt', 'bgr24',
    '-vcodec', 'rawvideo',
    '-an', '-sn',
    '-'
]

pipe = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, bufsize=10**8)
frame_size = FRAME_WIDTH * FRAME_HEIGHT * 3

# Detection state
cone1_y = None
cone2_y = None
armed = False
cross_time_1 = None
launch_point = None
cross_registered = False
result_text = ""
last_result_time = 0

# Logging setup
log_file = open("launch_log.csv", "a")
log_file.write("timestamp,speed_mph,result\n")

while True:
    raw_frame = pipe.stdout.read(frame_size)
    if len(raw_frame) != frame_size:
        print("Stream ended or frame incomplete.")
        break

    frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))
    overlay = frame.copy()
    status_message = "Waiting for ball..."

    # Run detection
    results = model(frame, verbose=False)[0]
    ball_detections = [r for r in results.boxes.data if int(r[-1]) == 32 and float(r[4]) > 0.25]

    center_y = None
    if ball_detections:
        ball = ball_detections[0]
        x1, y1, x2, y2 = map(int, ball[:4])
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        cv2.circle(overlay, (center_x, center_y), 10, (0, 255, 255), -1)
        cv2.putText(overlay, "Ball", (center_x + 10, center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        status_message = "Ball detected"

    if cone1_y is None or cone2_y is None:
        cv2.putText(overlay, "Click Cone 1, then Cone 2", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        def set_cones(event, x, y, flags, param):
            global cone1_y, cone2_y
            if event == cv2.EVENT_LBUTTONDOWN:
                if cone1_y is None:
                    cone1_y = y
                    print(f"Set Cone 1 at y={y}")
                elif cone2_y is None:
                    cone2_y = y
                    print(f"Set Cone 2 at y={y}")

        cv2.setMouseCallback("Launch Monitor", set_cones)
        if cv2.waitKey(1) == 27:
            break
        cv2.imshow("Launch Monitor", overlay)
        continue

    cv2.line(overlay, (0, cone1_y), (FRAME_WIDTH, cone1_y), (0, 0, 255), 2)
    cv2.line(overlay, (0, cone2_y), (FRAME_WIDTH, cone2_y), (255, 0, 0), 2)

    if center_y:
        if not armed and center_y < cone1_y:
            armed = True
            cross_registered = False
            launch_point = (center_x, center_y)
            status_message = "Armed"

        if armed and not cross_registered and center_y >= cone1_y:
            cross_time_1 = time.time()
            cross_registered = True
            cv2.circle(overlay, (center_x, cone1_y), 12, (0, 0, 255), 3)

        if armed and cross_time_1 and center_y >= cone2_y:
            cross_time_2 = time.time()
            elapsed = cross_time_2 - cross_time_1
            print(f"Cone 1 at {cross_time_1:.2f}, Cone 2 at {cross_time_2:.2f}, elapsed: {elapsed:.3f}s")
            speed_fps = CONE_DISTANCE_FT / elapsed
            speed_mph = speed_fps * MPH_CONVERSION

            t_goal = (GOAL_DISTANCE_YARDS * 3.0) / speed_fps
            pred_x = launch_point[0]
            pred_y = int(launch_point[1] - speed_fps * t_goal)

            goal_x = (FRAME_WIDTH - GOAL_WIDTH_PX) // 2
            goal_y = 50
            cv2.rectangle(overlay, (goal_x, goal_y), (goal_x + GOAL_WIDTH_PX, goal_y + GOAL_HEIGHT_PX), (0, 255, 0), 2)

            if goal_x <= pred_x <= goal_x + GOAL_WIDTH_PX and goal_y <= pred_y <= goal_y + GOAL_HEIGHT_PX:
                color = (0, 255, 0)
                result_text = f"GOAL ({speed_mph:.1f} MPH)"
                result_type = "GOAL"
            else:
                color = (0, 0, 255)
                result_text = f"MISS ({speed_mph:.1f} MPH)"
                result_type = "MISS"

            cv2.circle(overlay, (center_x, cone2_y), 12, (255, 0, 0), 3)
            cv2.circle(overlay, (pred_x, pred_y), 10, color, -1)
            status_message = result_text

            timestamp = datetime.now().isoformat()
            log_file.write(f"{timestamp},{speed_mph:.1f},{result_type}\n")
            log_file.flush()

            armed = False
            cross_time_1 = None
            last_result_time = time.time()

    if result_text:
        cv2.putText(overlay, result_text, (30, FRAME_HEIGHT - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        if time.time() - last_result_time > RESET_AFTER_SECONDS:
            result_text = ""
            result_type = ""

    cv2.putText(overlay, status_message, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
    cv2.imshow("Launch Monitor", overlay)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        cone1_y = None
        cone2_y = None
        armed = False
        cross_time_1 = None
        launch_point = None
        cross_registered = False
        result_text = ""

pipe.terminate()
log_file.close()
cv2.destroyAllWindows()