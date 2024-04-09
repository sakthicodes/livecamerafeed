from flask import Flask, render_template
import cv2
import base64
import threading
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# OpenCV video capture
cap = cv2.VideoCapture(0)

def emit_camera_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert frame to base64
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('frame', jpg_as_text)

# Thread for emitting camera frames
thread = threading.Thread(target=emit_camera_frames)
thread.daemon = True
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
