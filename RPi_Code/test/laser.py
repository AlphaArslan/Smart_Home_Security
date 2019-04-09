import RPi.GPIO as GPIO
import time

LASER_PIN = 15          ## BCM

GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_PIN, GPIO.OUT)

try:
    while True:
        if GPIO.input(LASER_PIN) is False:
            print("-- No Car Detected ")
        else :
            print("-- Car Detected ")
        time.sleep(2)
        
