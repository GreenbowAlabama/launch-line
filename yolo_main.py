from ultralytics import YOLO
import cv2
import time
import collections
import os

# Constants
CONE_DISTANCE_FT = 6.0
MPH_CONVERSION = 0.681818
CONE_TOLERANCE_PX = 15
MIN_DELAY_BETWEEN_CONES = 0.05
SAVE_FRAMES = True

# Setup
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
model = YOLO("yolov8s.pt")

# State variables
cone1_y = None
cone2_y = None
click_count = 0
armed = False
cross_time_1 = None
cross_time_2 = None
speed_ready = False
waiting_for_cone2 = False
previous_ball_y = None
speed_mph = None
ball_path = collections.deque(maxlen=50)
shot_speeds = collections.deque(maxlen=5)

# Click handler
def click_event(event, x, y, flags, params):
    global cone1_y, cone2_y, click_count
    if event == cv2.EVENT_LBUTTONDOWN:
        if click_count == 0:
            cone1_y = y
            click_count += 1
            print(f"Set Cone 1 (START - near kicker) at y={y}")
        elif click_count == 1:
            cone2_y = y
            click_count += 1
            print(f"Set Cone 2 (END - near camera) at y={y}")
            print("Direction is fixed: ball moves from top to bottom")
        else:
            print("Cones already set. Press 'r' to reset if needed.")

cv2.namedWindow("YOLO Ball Detection")
cv2.setMouseCallback("YOLO Ball Detection", click_event)

# Output folder for debug frames
if SAVE_FRAMES:
    os.makedirs("debug_frames", exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_time = time.time()
    results = model.track(source=frame, conf=0.3, classes=[32], persist=True, verbose=False)
    frame_display = frame.copy()

    if cone1_y is not None and cone2_y is not None:
        if results and len(results[0].boxes) > 0:
            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                ball_path.append((center_x, center_y))
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                print(f"Detected class {cls} with confidence {conf:.2f} at y={center_y}")

                cv2.rectangle(frame_display, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.putText(frame_display, f"BallY: {center_y}", (x1, y2 + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                if not armed and center_y < cone1_y - 20:
                    armed = True
                    print("System re-armed. (top-to-bottom)")

                if armed and cross_time_1 is None and previous_ball_y is not None:
                    if previous_ball_y < cone1_y <= center_y:
                        cross_time_1 = frame_time
                        waiting_for_cone2 = True
                        print(f"Cone 1 crossed at {cross_time_1:.2f}")
                        if SAVE_FRAMES:
                            cv2.imwrite(f"debug_frames/cone1_{int(cross_time_1)}.jpg", frame_display)

                if waiting_for_cone2 and cross_time_2 is None and previous_ball_y is not None:
                    if previous_ball_y < cone2_y <= center_y:
                        cross_time_2 = frame_time
                        if cross_time_2 - cross_time_1 >= MIN_DELAY_BETWEEN_CONES:
                            elapsed = cross_time_2 - cross_time_1
                            speed_mph = (CONE_DISTANCE_FT / elapsed) * MPH_CONVERSION
                            print(f"Ball Speed: {speed_mph:.2f} MPH")
                            speed_ready = True
                            waiting_for_cone2 = False
                            if SAVE_FRAMES:
                                cv2.imwrite(f"debug_frames/cone2_{int(cross_time_2)}.jpg", frame_display)
                        else:
                            print("Cone 2 crossing too soon — ignored")

                previous_ball_y = center_y

        # Cone lines
        cv2.line(frame_display, (0, cone1_y), (1280, cone1_y), (0, 0, 255), 2)
        cv2.putText(frame_display, "Cone 1 (START)", (10, cone1_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.line(frame_display, (0, cone2_y), (1280, cone2_y), (255, 0, 0), 2)
        cv2.putText(frame_display, "Cone 2 (END)", (10, cone2_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Ball path
        for pt in ball_path:
            cv2.circle(frame_display, pt, 3, (0, 255, 0), -1)

        if speed_ready:
            shot_speeds.appendleft(speed_mph)
            speed_ready = False

    else:
        cv2.putText(frame_display, "Click Cone 1 (start near kicker), then Cone 2 (near camera)", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    for i, spd in enumerate(shot_speeds):
        cv2.putText(frame_display, f"{spd:.2f} MPH", (1100, 50 + i * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    fps = cap.get(cv2.CAP_PROP_FPS)
    cv2.putText(frame_display, f"{fps:.1f} FPS", (10, 700),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("YOLO Ball Detection", frame_display)
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
        click_count = 0
        cone1_y = None
        cone2_y = None
        print("Reset detection state.")

cap.release()
cv2.destroyAllWindows()
