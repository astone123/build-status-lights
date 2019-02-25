import json
import os

STATE_PATH = os.path.join(os.getcwd(), 'build_state.json')

def save_state(theme_data):
    if os.path.exists(STATE_PATH):
        os.remove(STATE_PATH)
    with open(STATE_PATH, 'w') as f:
        f.write(json.dumps(theme_data))


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, 'r') as f:
            theme_data = json.load(f)
        return theme_data