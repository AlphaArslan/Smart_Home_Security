from flask import Flask, render_template, Response
import socket
from Communication import *

#start Flask app
app = Flask(__name__)

# create internal UDP socket to catch frames
sock = create_socket_receiving(4575)                                            # Hard Coded port

def web_stream():
    while True:
        frame_bytes , address = sock.recvfrom(65507)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(web_stream(),
                mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
