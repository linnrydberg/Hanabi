from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')  # will load our client code

@socketio.on('my event')
def handle_my_custom_event(data):
    print('Received message from client:', data)
    emit('my response', {'data': f"Server received: {data['data']}"})

@socketio.on('start counter')
def start_counter(data):
    print("starting counter")
    for i in range(10):
        emit('clock beep', {'time': i})
        time.sleep(1)




if __name__ == '__main__':
    socketio.run(app, debug=True)