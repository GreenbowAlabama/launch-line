# visualizer.py
import cv2

def draw_overlay(frame, tracker, result_text, status_message, frame_width, frame_height):
    overlay = frame.copy()

    # Draw cone lines using correct attributes
    if hasattr(tracker, "cone1_start") and hasattr(tracker, "cone1_end"):
        cv2.line(overlay, tracker.cone1_start, tracker.cone1_end, (0, 255, 255), 6)  # Bright yellow
    if hasattr(tracker, "cone2_start") and hasattr(tracker, "cone2_end"):
        cv2.line(overlay, tracker.cone2_start, tracker.cone2_end, (255, 0, 255), 6)  # Bright magenta

    # Draw result marker
    if tracker.last_result and 'prediction' in tracker.last_result:
        x, y = tracker.last_result['prediction']
        color = (0, 255, 0) if tracker.last_result['result'] == "GOAL" else (0, 0, 255)
        cv2.circle(overlay, (x, y), 10, color, -1)
        cv2.putText(overlay, tracker.last_result['result'], (x + 12, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Display result and status messages
    if result_text:
        cv2.putText(overlay, result_text, (30, frame_height - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    if status_message:
        cv2.putText(overlay, status_message, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

    return overlay