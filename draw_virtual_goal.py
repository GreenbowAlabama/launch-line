import cv2


def draw_virtual_goal(frame, projection_point_px, cone1_y, projection_visible):
    # Virtual goal dimensions in feet
    goal_width_ft = 8.0
    goal_height_ft = 8.0

    # Pixels per foot scale (estimated from cone spacing)
    frame_height = frame.shape[0]
    px_per_ft = abs(frame_height - cone1_y) / 10  # adjust 10 ft away goal projection

    goal_width_px = int(goal_width_ft * px_per_ft)
    goal_height_px = int(goal_height_ft * px_per_ft)

    if projection_point_px is None or not projection_visible:
        return frame

    # Projected landing point (bottom center of goal)
    proj_x, proj_y = int(projection_point_px[0]), int(projection_point_px[1])
    top_left = (proj_x - goal_width_px // 2, proj_y - goal_height_px)
    bottom_right = (proj_x + goal_width_px // 2, proj_y)

    # Clamp to image dimensions
    height, width = frame.shape[:2]
    top_left = (max(0, top_left[0]), max(0, top_left[1]))
    bottom_right = (min(width - 1, bottom_right[0]), min(height - 1, bottom_right[1]))

    # Draw goal box
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 255), 2)
    cv2.putText(frame, "Virtual Goal", (top_left[0], top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    return frame
