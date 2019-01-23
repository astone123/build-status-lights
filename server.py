from flask import Flask, request, abort

from config import Config

app = Flask(__name__)

config = Config()


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    repo_url = get_repo_url(data)
    branch_name = get_branch_name(data)
    if is_valid_repo_url(repo_url) and is_valid_branch(branch_name):
        print(repo_url)
        print(branch_name)
        print(get_build_status(data))
    return 'success', 200


def get_repo_url(data):
    return data.get('repository', {}).get('links', {}).get('html', {}).get('href', {})


def get_branch_name(data):
    return data.get('commit_status', {}).get('refname', {})


def get_build_status(data):
    return data.get('commit_status', {}).get('state', {})


def is_valid_repo_url(url):
    return not not next(project for project in config.projects if project["repo_url"] == url)


def is_valid_branch(branch_name):
    return not not next(project for project in config.projects if project["branch"] == branch_name)


if __name__ == '__main__':
    app.run()
