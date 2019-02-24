from flask import Flask, request
from flask_socketio import SocketIO
from flask_socketio import send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/', methods=['POST'])
def index():
    json_data = request.get_json()
    return json_data


@socketio.on('message')
def handle_message(message):
    send(message)

@socketio.on('json')
def handle_json(json):
    send(json, json=True)

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json)

if __name__ == '__main__':
    socketio.run(app)


