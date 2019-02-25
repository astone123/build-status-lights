import asyncio
import ssl

import websockets
import json
from config import Config
from bitbucket_webhook_data import BitbucketWebhookData
from build_indicator import BuildIndicator
from state import  load_state
import websocket

config = Config()
build_indicator = BuildIndicator(config)
previous_state = load_state()
if previous_state:
    build_indicator.update_theme(previous_state)

try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    webhookData = json.loads(message)
    print('received message')
    try:
        data = BitbucketWebhookData(webhookData, config)
        if data.is_valid_repo_url and data.is_valid_branch:
            print(data.repo_url)
            print(data.branch_name)
            print(data.build_status)
            build_indicator.update_project_status(data.repo_url, data.branch_name, data.build_status)
    except Exception as e:
        print(f"Error: {e}")

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        while True:
            continue
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    url = f"wss://{config.ws_server_hostname}:{config.ws_server_port}?apiKey={config.api_key}"
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
