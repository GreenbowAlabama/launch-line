# yolo_main_with_goal.py
import cv2
import math
import time
import numpy as np
from ultralytics import YOLO

# Constants
CONE_DISTANCE_FT = 8.0
MPH_CONVERSION = 0.681818
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
GOAL_DISTANCE_YARDS = 10
GOAL_WIDTH_PX = 250
GOAL_HEIGHT_PX = 100

# Load assets
soccer_field = cv2.imread('soccer_field.jpg')
background = cv2.resize(soccer_field, (FRAME_WIDTH, FRAME_HEIGHT))

# Load model
model = YOLO("yolov8n.pt")

# Use the RTSP stream served by MediaMTX
RTSP_STREAM_URL = "rtsp://4.255.67.198:8554/live/stream"
cap = cv2.VideoCapture(RTSP_STREAM_URL)

cone1_y = None
cone2_y = None
armed = False
cross_time_1 = None
speed_mph = None
launch_point = None
cross_registered = False
result_text = ""

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame from RTSP stream.")
        time.sleep(1)
        continue

    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    overlay = background.copy()

    # Get detections
    results = model(frame, verbose=False)[0]
    ball_detections = [r for r in results.boxes.data if int(r[-1]) == 32 and float(r[4]) > 0.25]

    center_y = None
    if ball_detections:
        ball = ball_detections[0]
        x1, y1, x2, y2 = map(int, ball[:4])
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.putText(overlay, "Ball", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    if cone1_y is None or cone2_y is None:
        cv2.putText(overlay, "Click Cone 1 (start), then Cone 2 (end)", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.imshow("Launch Sim", overlay)

        def set_cones(event, x, y, flags, param):
            global cone1_y, cone2_y
            if event == cv2.EVENT_LBUTTONDOWN:
                if cone1_y is None:
                    cone1_y = y
                    print(f"Set Cone 1 at y={y}")
                elif cone2_y is None:
                    cone2_y = y
                    print(f"Set Cone 2 at y={y}")

        cv2.setMouseCallback("Launch Sim", set_cones)
        if cv2.waitKey(1) == 27:
            break
        continue

    cv2.line(overlay, (0, cone1_y), (FRAME_WIDTH, cone1_y), (0, 0, 255), 2)
    cv2.line(overlay, (0, cone2_y), (FRAME_WIDTH, cone2_y), (255, 0, 0), 2)

    if center_y:
        if not armed and center_y < cone1_y:
            armed = True
            cross_registered = False
            launch_point = (center_x, center_y)
            print("System armed")

        if armed and not cross_registered and center_y >= cone1_y:
            cross_time_1 = time.time()
            print(f"Cone 1 crossed at {cross_time_1:.2f}")
            cross_registered = True

        if armed and cross_time_1 and center_y >= cone2_y:
            cross_time_2 = time.time()
            elapsed = cross_time_2 - cross_time_1
            speed_fps = CONE_DISTANCE_FT / elapsed
            speed_mph = speed_fps * MPH_CONVERSION
            print(f"Ball Speed: {speed_mph:.2f} MPH")

            # Predict goal hit
            t_goal = (GOAL_DISTANCE_YARDS * 3.0) / speed_fps
            pred_x = int(launch_point[0])
            pred_y = int(launch_point[1] + math.sin(-math.pi / 2) * speed_fps * t_goal)

            goal_x = (FRAME_WIDTH - GOAL_WIDTH_PX) // 2
            goal_y = 50
            cv2.rectangle(overlay, (goal_x, goal_y), (goal_x + GOAL_WIDTH_PX, goal_y + GOAL_HEIGHT_PX), (0, 255, 0), 2)

            if goal_x <= pred_x <= goal_x + GOAL_WIDTH_PX and goal_y <= pred_y <= goal_y + GOAL_HEIGHT_PX:
                color = (0, 255, 0)
                result_text = f"GOAL ({speed_mph:.1f} MPH)"
            else:
                color = (0, 0, 255)
                result_text = f"MISS ({speed_mph:.1f} MPH)"

            cv2.circle(overlay, (pred_x, pred_y), 10, color, -1)
            print(result_text)
            armed = False
            cross_time_1 = None

    if result_text:
        cv2.putText(overlay, result_text, (30, FRAME_HEIGHT - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    cv2.imshow("Launch Sim", overlay)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        cone1_y = None
        cone2_y = None
        armed = False
        cross_time_1 = None
        speed_mph = None
        launch_point = None
        cross_registered = False
        result_text = ""
        print("Reset detection state.")

cap.release()
cv2.destroyAllWindows()
