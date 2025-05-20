import os
from datetime import datetime

class KickLogger:
    def __init__(self, path="launch_log.csv"):
        is_new_file = not os.path.exists(path)
        self.file = open(path, "a")
        if is_new_file:
            self.file.write("timestamp,speed_mph,result\n")

    def log(self, result, result_type):
        timestamp = datetime.now().isoformat()
        self.file.write(f"{timestamp},{result['speed_mph']:.1f},{result_type}\n")
        self.file.flush()

    def close(self):
        self.file.close()