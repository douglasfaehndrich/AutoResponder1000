import json
import os

RESPONSES_FILE = os.path.join(os.path.dirname(__file__), "../responses.json")

def load_responses():
    with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_responses(responses):
    with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
        json.dump(responses, f, indent=4)
