from flask import Flask, Response, session, render_template, request, redirect, g, url_for
import socket
from Communication import *
import os

#start Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# create internal UDP socket to catch frames
sock = create_socket_receiving(4151)                                            # Hard Coded port

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

@app.route('/temp', methods=['GET', 'POST'])
def temp():
    # if request.method == 'POST':
    #     session.pop('user', None)
    #     if request.form['username'] == 'admin' and request.form['password'] == 'admin':
    #         return Response('Success')
    #     # print(request.form)
    return render_template("temp.html")


@app.route('/video_feed')
def video_feed():
    if g.user is None:
        return redirect(url_for('login'))
    return Response(web_stream(),
                mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    app.run(host='192.168.1.6', debug=True)
