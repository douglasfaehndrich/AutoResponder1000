import json
import os
import shutil
import sys

# Determine the base path (works for both .py and .exe)
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_PATH = os.path.dirname(sys.executable)
else:
    # Running as script
    BASE_PATH = os.path.dirname(os.path.dirname(__file__))

RESPONSES_FILE = os.path.join(BASE_PATH, "responses.json")
TEMPLATE_FILE = os.path.join(BASE_PATH, "responses.template.json")

def load_responses():
    # If responses.json doesn't exist, create it from template
    if not os.path.exists(RESPONSES_FILE):
        if os.path.exists(TEMPLATE_FILE):
            print(f"Creating {RESPONSES_FILE} from template...")
            shutil.copy(TEMPLATE_FILE, RESPONSES_FILE)
        else:
            raise FileNotFoundError(
                f"Neither {RESPONSES_FILE} nor {TEMPLATE_FILE} found!\n"
                "Please ensure responses.template.json is in the same folder as the application."
            )

    with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_responses(responses):
    with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
        json.dump(responses, f, indent=4)
