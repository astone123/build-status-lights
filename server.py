from flask import Flask, request, abort
from config import Config
from bitbucket_webhook_data import BitbucketWebhookData

app = Flask(__name__)

config = Config()

@app.route('/', methods=['POST'])
def webhook():
    data = BitbucketWebhookData(request.get_json(), config)
    if data.is_valid_repo_url and data.is_valid_branch:
        print(data.repo_url)
        print(data.branch_name)
        print(data.build_status)
    return 'success', 200


if __name__ == '__main__':
    app.run()
