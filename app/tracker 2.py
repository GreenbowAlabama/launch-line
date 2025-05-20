# tracker.py
class BallTracker:
    def __init__(self, cone_distance_ft, mph_conversion, fps=30):
        self.default_cone1_x = None
        self.default_cone2_x = None
        self.cone1_x = None
        self.cone2_x = None
        self.armed = False
        self.cross_frame_1 = None
        self.cross_registered = False
        self.launch_point = None
        self.last_result = None
        self.mph_conversion = mph_conversion
        self.cone_distance_ft = cone_distance_ft
        self.goal_distance_yards = 10
        self.goal_width_px = 250
        self.goal_height_px = 100
        self.frame_height = 720
        self.goal_y = 50
        self.fps = fps

    def set_static_cones(self, cone1_x, cone2_x):
        self.cone1_x = cone1_x
        self.cone2_x = cone2_x
        self.default_cone1_x = cone1_x
        self.default_cone2_x = cone2_x
        print(f"[STATIC CONES] Cone 1 set to x={cone1_x}, Cone 2 set to x={cone2_x}")

    def reset_cones(self):
        self.cone1_x = self.default_cone1_x
        self.cone2_x = self.default_cone2_x
        self.default_cone1_x = None
        self.default_cone2_x = None

    def update(self, center_x, center_y, current_frame):
        status = "Waiting for ball"
        result = None

        if self.cone1_x is None or self.cone2_x is None:
            return status, None

        if not self.armed and center_x < self.cone1_x:
            self.armed = True
            self.cross_registered = False
            self.launch_point = (center_x, center_y)
            print(f"[ARMED] Ball seen before Cone 1 at x={center_x}")
            status = "Armed"

        if self.armed and not self.cross_registered and center_x >= self.cone1_x:
            self.cross_frame_1 = current_frame
            self.cross_registered = True
            print(f"[CONE 1 CROSSED] at x={center_x} (frame {current_frame})")
            status = "Crossed Cone 1"

        if self.armed and self.cross_frame_1 is not None and center_x >= self.cone2_x:
            cross_frame_2 = current_frame
            frame_diff = cross_frame_2 - self.cross_frame_1
            elapsed = frame_diff / self.fps
            print(f"[CONE 2 CROSSED] at x={center_x} (frame {current_frame}), elapsed={elapsed:.3f}s")

            speed_fps = self.cone_distance_ft / elapsed
            speed_mph = speed_fps * self.mph_conversion

            # Goal projection
            t_goal = (self.goal_distance_yards * 3.0) / speed_fps
            pred_x = int(self.launch_point[0] + speed_fps * t_goal)
            pred_y = self.launch_point[1]

            goal_x1 = pred_x - self.goal_width_px // 2
            goal_x2 = pred_x + self.goal_width_px // 2
            goal_y1 = self.goal_y
            goal_y2 = self.goal_y + self.goal_height_px

            in_goal = goal_y1 <= pred_y <= goal_y2
            result_type = "GOAL" if in_goal else "MISS"
            status = f"{result_type} ({speed_mph:.1f} MPH)"

            print(f"[RESULT] {status} | Predicted impact: ({pred_x}, {pred_y})")

            result = {
                "speed_mph": speed_mph,
                "frame": current_frame,
                "launch_point": self.launch_point,
                "prediction": (pred_x, pred_y),
                "result": result_type
            }

            self.armed = False
            self.cross_frame_1 = None

        return status, result
