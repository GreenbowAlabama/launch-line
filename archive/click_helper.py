import cv2

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked at: ({x}, {y})")

cap = cv2.VideoCapture("./recordings/test_kick.mp4")  # or replace with your video path
ret, frame = cap.read()

if ret:
    cv2.imshow("Test Frame", frame)
    cv2.setMouseCallback("Test Frame", click_event)
    print("Click anywhere on the frame to get pixel coordinates...")
    cv2.waitKey(0)

cv2.destroyAllWindows()
cap.release()