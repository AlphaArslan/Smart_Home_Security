##################### IMPORT #####################
from flask import Flask, Response, session, render_template, request, redirect, g, url_for
import socket
from Communication import *
import os

##################### Global #####################
# control panel
FRAMES_PORT = 4575
RPI_PORT  = 5532
RIGHT_COMMAND = 'R'
LEFT_COMMAND  = 'L'
RPI_ADDRESS = '192.168.1.7'

temp_data  = [26, 27, 26, 25, 26, 27, 27, 28, 27, 26, 27, 26]
smoke_data = [1, 2, 1, 2, 3, 4, 3, 0, 1, 2, 0]

# start Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# create internal UDP socket to catch frames
sock = create_socket_receiving(FRAMES_PORT)                                            # Hard Coded port
servo_sock = create_socket()

################### Funcutions ###################
def web_stream():
    while True:
        frame_bytes , address = sock.recvfrom(65507)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/')
def index():
    if g.user is None:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['user'] = request.form['username']
            return redirect('/')
    return render_template("login.html")

@app.route('/logout')
def Logout():
    session.pop('user')
    return redirect(url_for('login'))

######### INCOMPLETE
@app.route('/change_creds', methods=['GET', 'POST'])
def change_creds():
    if g.user is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        session.pop('user', None)
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['user'] = request.form['username']
            return redirect('/')
    return render_template("login.html")

@app.route('/sensors')
def sensors():
    return render_template('sensor.html', TEMP_DATA = temp_data, SMOKE_DATA = smoke_data)


@app.route('/video_feed')
def video_feed():
    if g.user is None:
        return redirect(url_for('login'))
    return Response(web_stream(),
                mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_stream')
def video_stream():
    if g.user is None:
        return redirect(url_for('login'))
    return render_template('stream.html')

@app.route('/servo_right')
def servo_right():
    print("Servo Right Command")
    servo_sock.sendto(RIGHT_COMMAND.encode('ascii'), (RPI_ADDRESS, RPI_PORT))
    return render_template('stream.html')

@app.route('/servo_left')
def servo_left():
    print("Servo Left Command")
    servo_sock.sendto(LEFT_COMMAND.encode('ascii'), (RPI_ADDRESS, RPI_PORT))
    return render_template('stream.html')


@app.route('/scope')
def scope():
    return render_template('scope.html')

@app.route('/contact_me')
def contact_me():
    return render_template('contact_me.html')

###################### loop ######################
if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    app.run(host='0.0.0.0', debug=True)
