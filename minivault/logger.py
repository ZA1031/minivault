import os
import json

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "log.jsonl")

os.makedirs(LOG_DIR, exist_ok=True)

def log_interaction(entry: dict):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
