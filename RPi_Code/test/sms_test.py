import serial
import time


# creating serial communication port for the GSM module
phone = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1.0)

def send_sms_alert():
    phone.write(b'AT+CMGF=1\r')
    result=phone.read(100)
    print(result)

    phone.write('AT+CMGS=\"87422459\"\r')
    phone.write('this is an alert')
    result=phone.read(100)
    print(result)
    print("SMS sent")

if __name__ == '__main__':
    print("sending SMS...")
    send_sms_alert()
