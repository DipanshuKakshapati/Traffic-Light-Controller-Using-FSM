from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)  # Enable CORS
socketio = SocketIO(app, cors_allowed_origins="*")

states = {"Red": 5, "Green": 15, "Yellow": 15}
current_state = "Red"
active = False  # Control activation based on user interaction

@app.route('/')
def index():
    return render_template('traffic_light.html')

@socketio.on('start_traffic_light')
def handle_start_traffic_light():
    global active
    if not active:
        active = True
        traffic_light_fsm()

def traffic_light_fsm():
    global current_state, active
    while active:
        countdown = states[current_state]
        while countdown > 0:
            socketio.emit('new_state', {'state': current_state, 'timer': countdown})
            time.sleep(1)
            countdown -= 1
        if current_state == "Red":
            current_state = "Green"
        elif current_state == "Green":
            current_state = "Yellow"
        elif current_state == "Yellow":
            current_state = "Red"

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
