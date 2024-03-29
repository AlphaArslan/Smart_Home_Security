##################### IMPORT #####################
import socket
import netifaces as ni
import pantilthat

import serial
import time

from Communication import *

##################### Global #####################
# control panel
RIGHT_COMMAND     = 'R'
LEFT_COMMAND      = 'L'
# UNKNOWN_COMMAND   = 'U'
NETWORK_INTERFACE = 'wlan0'
COMMAND_PORT      = 5532

# PHONE_NUMBER = "+201553801503"

current_angle = 0

# getting ip of rpi through wlan0 interface
IP = ni.ifaddresses(NETWORK_INTERFACE)[2][0]['addr']

# create internal UDP socket to catch commands
sock = create_socket_receiving(COMMAND_PORT, host=IP)                                            # Hard Coded port

# creating serial communication port for the GSM module
# phone = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1.0)

################### Funcutions ###################

# def send_sms_alert():
#     phone.write(b'AT+CMGF=1\r')
#     result=phone.read(100)
#     print(result)
#
#     phone.write('AT+CMGS=\"87422459\"\r')
#     phone.write('this is an alert')
#     result=phone.read(100)
#     print(result)
#     print("SMS sent")

##################### setup ######################

# setting the initial servo angle
pantilthat.servo_one(current_angle)

###################### loop ######################
if __name__ == '__main__':
    while True:
        # listen for commands
        print("-- Listening ")
        data , address = sock.recvfrom(15)
        data = data.decode('ascii')
        print(data)

        if data is RIGHT_COMMAND :
            if current_angle is 90 :
                print('-- Already reached maximum angle to the right')
            else :
                current_angle += 10
                pantilthat.servo_one(current_angle)

        elif data is LEFT_COMMAND :
            if current_angle == -90 :
                print('-- Already reached maximum angle to the left')
            else :
                current_angle -= 10
                pantilthat.servo_one(current_angle)

        # elif data is UNKNOWN_COMMAND:
        #     send_sms_alert()
