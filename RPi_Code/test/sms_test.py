import serial
import time


PHONE_NUMBER = "+201553801503"


# creating serial communication port for the GSM module
phone = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1.0)

def send_sms_alert():
    phone.write('AT+CPIN=0000\r\n')
    result=phone.read(100)
    print(result)

    phone.write('AT+CMGS="' + PHONE_NUMBER +'"\r\n')
    phone.write('this is an alert')
    result=phone.read(100)
    print(result)
    print("SMS sent")

if __name__ == '__main__':
    print("sending SMS...")
    send_sms_alert()
