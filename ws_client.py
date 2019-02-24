import asyncio
import websockets
import json
from config import Config
from bitbucket_webhook_data import BitbucketWebhookData
from build_indicator import BuildIndicator

config = Config()
build_indicator = BuildIndicator(config)

async def processWebhook():
    async with websockets.connect(
            f'ws://{config.ws_server_hostname}:{config.ws_server_port}?apiKey={config.api_key}') as websocket:

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