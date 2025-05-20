import yaml
import os

def load_lab_config():
    config_path = os.path.join(os.path.dirname(__file__), "config/lab_config.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)