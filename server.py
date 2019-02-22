import os
import json
from flask import Flask, request, abort
from config import Config
from bitbucket_webhook_data import BitbucketWebhookData
from build_indicator import BuildIndicator

app = Flask(__name__)
STATE_PATH = os.path.join(os.getcwd(), 'build_state.json')

config = Config()
build_indicator = BuildIndicator(config)


def inspect(r):
    print('----------------------')
    print(r.headers)
    print(r.data)
    print('----------------------')

@app.route('/', methods=['POST'])
def webhook():
    data = BitbucketWebhookData(request.get_json(), config)
    inspect(request)
    if data.is_valid_repo_url and data.is_valid_branch:
        print(data.repo_url)
        print(data.branch_name)
        print(data.build_status)
        build_indicator.update_project_status(data.repo_url,data.branch_name, data.build_status)
        return 'success', 200
    return 400


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


if __name__ == '__main__':
    previous_state = load_state()
    if previous_state:
        build_indicator.update_theme(previous_state)
    app.run()
