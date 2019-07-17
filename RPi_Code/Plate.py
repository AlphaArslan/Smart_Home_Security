##################### IMPORT #####################
import RPi.GPIO as GPIO
import picamera
import requests
import base64
import json
import time
import os
import smtplib, ssl

import sqlite3
import control_DB
from Communication import *

##################### Global #####################
#constants
PWD         = os.path.dirname(os.path.realpath(__file__))       #returns path to project folder
DB_PATH     = 'database.db'
api_url     = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=sk_d1f041e7fe7cef9f91f69fad'
plate1      = "plate1"
plate2      = "plate3"
plate3      = "plate3"
DELAY       = 5                                                 # time for servo opening

SMTP_PORT = 465  # For SSL
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "dev.script.21@gmail.com"  # Enter your address
RECEIVER_EMAIL = "bluphanc@gmail.com"  # Enter receiver address
SENDER_PASS = "0.9millidev"
EMAIL_CONTENT = """\
Subject: Warning

Unkown Car detected."""

# creating serial communication port for the GSM module
phone = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1.0)

# Pin Configuration
servo_pin = 11
LASER     = 13
DETECTOR  = 15

################### Funcutions ###################
def wait_for_cars():
    while GPIO.input(DETECTOR) is True:
        print('--- Waiting for cars')
        time.sleep(1)

def check_plates(plate1, plate2, plate3):
    c.execute("SELECT * FROM cars")
    s = c.fetchone()
    while s is not None:
        if s[1] in (plate1, plate2, plate3):
            return True
        s = c.fetchone()
    return False

def send_email():
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, EMAIL_CONTENT)

def get_ip(interface_name):
    """Helper to get the IP adresse of the running server
    """
    import netifaces as ni
    ip = ni.ifaddresses(interface_name)[2][0]['addr']
    return ip  # should print "192.168.100.37"


##################### setup ######################
# setting up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LASER ,GPIO.OUT)
GPIO.setup(DETECTOR ,GPIO.IN)
GPIO.setup(servo_pin, GPIO.OUT)
servo_pwm = GPIO.PWM(servo_pin, 50)                 #Servo PWM
servo_pwm.start(0)

######## database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
control_DB.init_db()

######## socket
sock = create_socket()
sock.settimeout(1)
port = 1080
host = get_ip("wlan0")

###################### loop ######################
while True :
        ######## wait for cars [laser detector]
        wait_for_cars()

        ######## get the frame
        img_base64 = get_frames_base64(host, port, sock)
        print("--  Picture token")

        ######## process the image to get plates
        # with open(IMAGE_PATH, 'rb') as image_file:
        #         img_base64 = base64.b64encode(image_file.read())

        print("--  sending image online")
        flag = True
        while flag:
                try:
                        r = requests.post(api_url, data = img_base64)
                except requests.exceptions.ConnectionError:
                        print("XX  Connection lost .. Please reconnect")
                        time.sleep(1)
                else:			#no problem occuered
                        flag = False
                        print("--  Connected .. waiting results")
        r = r.json()

        if (len(r["results"]) == 0):
            print("-   No cars seen")
            continue

        plate1 = r["results"][0]["plate"]
        try:
                plate2 = r["results"][0]["candidates"][1]["plate"]
        except IndexError:
                plate2 = "No_plate"
        try:
                plate3 = r["results"][0]["candidates"][2]["plate"]
        except IndexError:
                plate3 = "No_plate"

        print("-   Plate Guess 1 :" + plate1 )
        print("-   Plate Guess 2 :" + plate2 )
        print("-   Plate Guess 3 :" + plate3 )

        ######## check the plate number
         if check_plates(plate1, plate2, plate3) is False:
             send_email()
