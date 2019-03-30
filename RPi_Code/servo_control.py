##################### IMPORT #####################
import socket
import netifaces as ni
import RPi.GPIO as GPIO
from Communication import *


##################### Global #####################
# control panel
RIGHT_COMMAND     = 'R'
LEFT_COMMAND      = 'L'
NETWORK_INTERFACE = 'wlan0'
SERVO_PORT        = 5532

# variable to hold the cuurent angle value
current_angle = 90

# getting ip of rpi through wlan0 interface
IP = ni.ifaddresses(NETWORK_INTERFACE)[2][0]['addr']

# create internal UDP socket to catch commands
sock = create_socket_receiving(SERVO_PORT, host=IP)                                            # Hard Coded port


# Pin Configuration GPIO.BOARD
servo_pin = 11


################### Funcutions ###################
def servo_angle(angle):
    duty = angle/18 + 2.5
    GPIO.output(servo_pin, True)
    servo_pwm.ChangeDutyCycle(duty)


##################### setup ######################
# setting up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)
servo_pwm = GPIO.PWM(servo_pin, 50)                 #Servo PWM
servo_pwm.start(0)

# setting the initial servo angle
servo_angle(current_angle)

###################### loop ######################
if __name__ == '__main__':
    while True:
        # listen for commands
        data , address = sock.recvfrom(15)
        data = data.decode('ascii')
        if data is RIGHT_COMMAND :
            if current_angle is 180 :
                print('-- Already reached maximum angle to the right')
            else :
                current_angle += 10
                servo_angle(current_angle)
        elif data is LEFT_COMMAND :
            if current_angle is 0 :
                print('-- Already reached maximum angle to the left')
            else :
                current_angle -= 10
                servo_angle(current_angle)
