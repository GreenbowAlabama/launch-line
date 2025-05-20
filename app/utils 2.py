# app/utils.py

import json
import os

def load_lab_config(config_path="config/lab_config.json"):
    with open(config_path, "r") as f:
        return json.load(f)