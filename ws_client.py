import asyncio
import websockets
import json
import ssl
from config import Config
from bitbucket_webhook_data import BitbucketWebhookData
from build_indicator import BuildIndicator
from state import save_state, load_state

config = Config()
build_indicator = BuildIndicator(config)

ssl_context = ssl.SSLContext()
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.check_hostname = False

async def processWebhook():
    previous_state = load_state()
    if previous_state:
        build_indicator.update_theme(previous_state)

    url = f'wss://{config.ws_server_hostname}:{config.ws_server_port}?apiKey={config.api_key}'

    print(f'WSS URL {url}')

    async with websockets.connect(url, ssl=ssl_context) as websocket:

        print('Connecting to server with ws...')

        while True:
            webhookData = await websocket.recv()
            print(f"< {webhookData}")

            try:
                webhookData = json.loads(webhookData)
                data = BitbucketWebhookData(webhookData, config)
                if data.is_valid_repo_url and data.is_valid_branch:
                    print(data.repo_url)
                    print(data.branch_name)
                    print(data.build_status)
                    build_indicator.update_project_status(data.repo_url,data.branch_name, data.build_status)
            except Exception as e:
                print(f"Error: {e}")


asyncio.get_event_loop().run_until_complete(processWebhook())
