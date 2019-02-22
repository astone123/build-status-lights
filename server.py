from flask import Flask, request, abort
from config import Config
from bitbucket_webhook_data import BitbucketWebhookData
from build_indicator import BuildIndicator

app = Flask(__name__)

config = Config()
build_indicator = BuildIndicator(config)

def inspect(r):
    print('----------------------')
    print(r.headers)
    print(r.data)
    print('----------------------')

def permit(r):
    api_key = r.headers.get('X-Api-Key', None)
    if api_key is None:
        return False
    if api_key == config.api_key:
        return True
    return False


@app.route('/', methods=['POST'])
def webhook():
    data = BitbucketWebhookData(request.get_json(), config)
    inspect(request)
    if permit(r) is False:
        return 'unauthorized', 401
    if data.is_valid_repo_url and data.is_valid_branch:
        print(data.repo_url)
        print(data.branch_name)
        print(data.build_status)
        build_indicator.update_project_status(data.repo_url,data.branch_name, data.build_status)
        return 'success', 200
    return 'bad request', 400


if __name__ == '__main__':
    app.run()
