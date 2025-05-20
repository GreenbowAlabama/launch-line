# visualizer.py
import cv2

def draw_overlay(frame, tracker, result_text, status_message, frame_width, frame_height):
    overlay = frame.copy()

    print(f"Cone 1 f: {tracker.cone1_line}")
    print(f"Cone 2 f: {tracker.cone2_line}")

    # Draw diagonal/static cone lines
    if hasattr(tracker, "cone1_line"):
        cv2.line(overlay, tracker.cone1_line[0], tracker.cone1_line[1], (0, 255, 0), 2)

    if hasattr(tracker, "cone2_line"):
        cv2.line(overlay, tracker.cone2_line[0], tracker.cone2_line[1], (255, 0, 0), 2)

    # Draw result prediction (goal/miss)
    if tracker.last_result and 'prediction' in tracker.last_result:
        x, y = tracker.last_result['prediction']
        color = (0, 255, 0) if tracker.last_result['result'] == "GOAL" else (0, 0, 255)
        cv2.circle(overlay, (x, y), 10, color, -1)
        cv2.putText(overlay, tracker.last_result['result'], (x + 12, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Draw result text
    if result_text:
        cv2.putText(overlay, result_text, (30, frame_height - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    # Draw status (e.g. Tracking..., Armed, etc.)
    if status_message:
        cv2.putText(overlay, status_message, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

    return overlay