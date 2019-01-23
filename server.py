from flask import Flask, request, abort

from config import Config

app = Flask(__name__)

config = Config()

@app.route('/', methods=['POST'])
def webhook():
	print(request.json)
	data = request.get_json()
	print(data.get('repository', {}).get('links', {}).get('html', {}).get('href', {}))
	print(next(project for project in config.projects if project["repo_url"] == data.get('repository', {}).get('links', {}).get('html', {}).get('href', {})))
	return 'success', 200


if __name__ == '__main__':
	app.run()

