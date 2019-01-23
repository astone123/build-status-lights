from flask import Flask, request, abort
import yaml

app = Flask(__name__)

with open("config.yaml", 'r') as stream:
    try:
        PROJECTS = yaml.load(stream).get('projects', [])
    except yaml.YAMLError as exc:
        print(exc)

@app.route('/', methods=['POST'])
def webhook():
	print(request.json)
	data = request.get_json()
	print(data.get('repository', {}).get('links', {}).get('html', {}).get('href', {}))
	print(next(project for project in PROJECTS if project["repo_url"] == data.get('repository', {}).get('links', {}).get('html', {}).get('href', {})))
	return 'success', 200


if __name__ == '__main__':
	app.run()

