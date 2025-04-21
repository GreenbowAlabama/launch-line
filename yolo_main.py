from ultralytics import YOLO
import cv2

# Load model
model = YOLO("yolov8n.pt")  # Or a custom model if trained on your soccer ball

# Open camera
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(source=frame, conf=0.5, classes=[32], verbose=False)  # class 32 = sports ball
    annotated_frame = results[0].plot()

    cv2.imshow("YOLO Ball Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
