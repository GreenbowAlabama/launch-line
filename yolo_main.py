from ultralytics import YOLO
import cv2
import time
import collections

# Constants
CONE_DISTANCE_FT = 8.0
MPH_CONVERSION = 0.681818
CONE_TOLERANCE_PX = 15
MIN_DELAY_BETWEEN_CONES = 0.05  # seconds

# Detection state variables
cross_time_1 = None
cross_time_2 = None
speed_mph = None
waiting_for_cone2 = False
speed_ready = False
previous_ball_y = None
armed = False
cone1_above_cone2 = None

# Cone positions (set dynamically)
cone1_y = None
cone2_y = None

# CONFIG: Camera input
USE_RTSP = False
RTSP_URL = "rtsp://username:password@camera_ip_address:554/stream"

# Setup camera capture
cap = cv2.VideoCapture(RTSP_URL if USE_RTSP else 1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# YOLO model
model = YOLO("yolov8n.pt")

# Setup ball path and speed logs
ball_path = collections.deque(maxlen=30)
shot_speeds = collections.deque(maxlen=5)

# FPS tracking
prev_time = time.time()
frame_count = 0
fps = 0

# Click handler to set cones
click_count = 0
def click_event(event, x, y, flags, params):
    global cone1_y, cone2_y, click_count, cone1_above_cone2
    if event == cv2.EVENT_LBUTTONDOWN:
        click_count += 1
        if click_count == 1:
            cone1_y = y
            print(f"Set Cone 1 (START) at y={y}")
        elif click_count == 2:
            cone2_y = y
            print(f"Set Cone 2 (END) at y={y}")
            cone1_above_cone2 = cone1_y < cone2_y
            print(f"Direction set: {'top-to-bottom' if cone1_above_cone2 else 'bottom-to-top'}")

cv2.namedWindow("YOLO Ball Detection")
cv2.setMouseCallback("YOLO Ball Detection", click_event)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(source=frame, conf=0.3, classes=[32], persist=True, verbose=False)

    if cone1_y is not None and cone2_y is not None:
        if results and len(results[0].boxes) > 0:
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.putText(frame, "Ball", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                ball_y = int((y1 + y2) / 2)

                if not armed and cross_time_1 is None:
                    if cone1_above_cone2 and ball_y > cone1_y + 20:
                        armed = True
                        print("System re-armed. (top-to-bottom)")
                    elif not cone1_above_cone2 and ball_y < cone1_y - 20:
                        armed = True
                        print("System re-armed. (bottom-to-top)")

                cone1_cross = (
                    cone1_above_cone2 and previous_ball_y is not None and previous_ball_y < cone1_y <= ball_y or
                    not cone1_above_cone2 and previous_ball_y is not None and previous_ball_y > cone1_y >= ball_y
                )

                if armed and cross_time_1 is None and cone1_cross:
                    cross_time_1 = time.time()
                    waiting_for_cone2 = True
                    print(f"Cone 1 crossed at {cross_time_1:.2f}")

                cone2_cross = (
                    cone1_above_cone2 and previous_ball_y is not None and previous_ball_y < cone2_y <= ball_y or
                    not cone1_above_cone2 and previous_ball_y is not None and previous_ball_y > cone2_y >= ball_y
                )

                if waiting_for_cone2 and cross_time_2 is None and cone2_cross:
                    current_time = time.time()
                    if current_time - cross_time_1 >= MIN_DELAY_BETWEEN_CONES:
                        cross_time_2 = current_time
                        print(f"Cone 2 crossed at {cross_time_2:.2f}")

                        elapsed = cross_time_2 - cross_time_1
                        if elapsed > 0:
                            speed_fps = CONE_DISTANCE_FT / elapsed
                            speed_mph = speed_fps * MPH_CONVERSION
                            print(f"Ball Speed: {speed_mph:.2f} MPH")

                        speed_ready = True
                        waiting_for_cone2 = False
                    else:
                        print("Cone 2 crossing too soon — ignored")

                previous_ball_y = ball_y
                ball_path.append(((x1 + x2) // 2, (y1 + y2) // 2))

        cv2.line(frame, (0, cone1_y), (1280, cone1_y), (0, 0, 255), 2)
        cv2.putText(frame, "Cone 1", (10, cone1_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.line(frame, (0, cone2_y), (1280, cone2_y), (255, 0, 0), 2)
        cv2.putText(frame, "Cone 2", (10, cone2_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        if speed_mph is not None:
            cv2.putText(frame, f"Speed: {speed_mph:.2f} MPH", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        if speed_ready:
            shot_speeds.appendleft(speed_mph)
            speed_ready = False

    else:
        cv2.putText(frame, "Click to set Cone 1 and Cone 2", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

    for pt in ball_path:
        cv2.circle(frame, pt, 3, (0, 255, 0), -1)

    for i, spd in enumerate(shot_speeds):
        cv2.putText(frame, f"{spd:.2f} MPH", (1100, 50 + i * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.putText(frame, f"{fps:.1f} FPS", (10, 700),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("YOLO Ball Detection", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        cross_time_1 = None
        cross_time_2 = None
        speed_mph = None
        waiting_for_cone2 = False
        speed_ready = False
        previous_ball_y = None
        armed = False
        print("Reset detection state.")

cap.release()
cv2.destroyAllWindows()
