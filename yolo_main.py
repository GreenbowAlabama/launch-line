from ultralytics import YOLO
import cv2
import time

# Constants
CONE_DISTANCE_FT = 6.0
MPH_CONVERSION = 0.681818
CONE_TOLERANCE_PX = 15

# Detection state variables
cross_time_1 = None
cross_time_2 = None
speed_mph = None
waiting_for_cone2 = False
speed_ready = False
previous_ball_y = None

# Cone positions (set dynamically)
cone1_y = None  # red (garage door / top of frame)
cone2_y = None  # blue (camera side / bottom of frame)

# Click handler to set cone lines
click_count = 0
def click_event(event, x, y, flags, params):
    global cone1_y, cone2_y, click_count
    if event == cv2.EVENT_LBUTTONDOWN:
        click_count += 1
        if click_count == 1:
            cone1_y = y
            print(f"Set Cone 1 (START) at y={y}")
        elif click_count == 2:
            cone2_y = y
            print(f"Set Cone 2 (END) at y={y}")

# Load model
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

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

                # Draw box around ball
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.putText(frame, "Ball", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                # Display confidence score
                # conf = float(box.conf[0])
                # cv2.putText(frame, f"{conf:.2f}", (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

                # Calculate vertical center of ball
                ball_y = int((y1 + y2) / 2)

                # START: Detect crossing Cone 1 (start) from bottom
                if cross_time_1 is None and previous_ball_y and \
                    previous_ball_y > cone1_y >= ball_y:
                    cross_time_1 = time.time()
                    waiting_for_cone2 = True
                    print("Ball crossed Cone 1 (start) moving upward")

                # STOP: Detect crossing Cone 2 (end) from bottom
                elif waiting_for_cone2 and cross_time_2 is None and previous_ball_y and \
                    previous_ball_y > cone2_y >= ball_y:
                    cross_time_2 = time.time()
                    print("Ball crossed Cone 2 (end) moving upward")

                    elapsed = cross_time_2 - cross_time_1
                    if elapsed > 0:
                        speed_fps = CONE_DISTANCE_FT / elapsed
                        speed_mph = speed_fps * MPH_CONVERSION
                        print(f"Ball Speed: {speed_mph:.2f} MPH")

                    speed_ready = True
                    waiting_for_cone2 = False

                # Save position for next frame
                previous_ball_y = ball_y

        # Draw cone lines
        cv2.line(frame, (0, cone1_y), (1280, cone1_y), (0, 0, 255), 2)
        cv2.putText(frame, "Cone 1", (10, cone1_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.line(frame, (0, cone2_y), (1280, cone2_y), (255, 0, 0), 2)
        cv2.putText(frame, "Cone 2", (10, cone2_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Show speed if ready
        if speed_mph is not None:
            cv2.putText(frame, f"Speed: {speed_mph:.2f} MPH", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    else:
        cv2.putText(frame, "Click to set Cone 1 and Cone 2", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

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
        print("Reset detection state.")

cap.release()
cv2.destroyAllWindows()
