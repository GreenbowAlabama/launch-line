import cv2
import numpy as np

# Constants
DISTANCE_METERS = 1.8288  # 6 feet
cap = cv2.VideoCapture(0)  # External camera (change index if needed)

# Set resolution and FPS
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

fps = cap.get(cv2.CAP_PROP_FPS)
print("Camera FPS:", fps)

cv2.namedWindow("Ball Tracking", cv2.WINDOW_NORMAL)
cv2.namedWindow("Ball Mask", cv2.WINDOW_NORMAL)

# Dual HSV detection: white surface + colorful trim
lower_white = np.array([0, 0, 200])
upper_white = np.array([179, 80, 255])

lower_trim = np.array([5, 90, 130])
upper_trim = np.array([35, 255, 255])

ball_detected = False
start_frame = end_frame = None
frame_counter = 0
last_ball_x = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Could not read frame from camera.")
        break

    frame_counter += 1
    print(f"[DEBUG] Frame {frame_counter} captured.")

    frame_blur = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)

    # Create white + trim masks and combine
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_trim = cv2.inRange(hsv, lower_trim, upper_trim)
    mask = cv2.bitwise_or(mask_white, mask_trim)

    # Display mask and original feed
    cv2.imshow("Ball Mask", mask)
    cv2.imshow("Ball Tracking", frame)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"[DEBUG] Contours found: {len(contours)}")

    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        area = cv2.contourArea(contour)
        circle_area = np.pi * (radius ** 2)
        circularity = area / circle_area if circle_area > 0 else 0

        if 10 < radius < 40 and circularity > 0.6:
            print(f"[DEBUG] Ball candidate — radius: {radius:.2f}, circularity: {circularity:.2f}")
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)

            if not ball_detected:
                if last_ball_x is None:
                    last_ball_x = x
                elif abs(x - last_ball_x) > 50:
                    ball_detected = True
                    start_frame = frame_counter
                    print(f"[DEBUG] Ball moved — Start frame: {start_frame}")
            else:
                if end_frame is None and abs(x - last_ball_x) > 100:
                    end_frame = frame_counter
                    print(f"[DEBUG] End frame: {end_frame}")
                    break


    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("[INFO] Q pressed — exiting.")
        break

cap.release()
cv2.destroyAllWindows()

# Final speed calculation
if start_frame and end_frame:
    time_seconds = (end_frame - start_frame) / fps
    speed_mps = DISTANCE_METERS / time_seconds
    speed_fps = speed_mps * 3.28084
    speed_mph = speed_mps * 2.23694

    print("\n✅ Ball Speed:")
    print(f"  {speed_mps:.2f} m/s")
    print(f"  {speed_fps:.2f} ft/s")
    print(f"  {speed_mph:.2f} mph")
else:
    print("⚠️ Ball not tracked correctly.")
