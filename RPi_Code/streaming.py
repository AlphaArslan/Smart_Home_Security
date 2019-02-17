################### IMPORT
import socket
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

################### Function
def getpublickey():
    pubKey = tuple(map(int,input("Enter publicKey q, n : ").split(',')))
    return pubKey

def RSAencrypt(data):
    return data

def captureFrame():
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    return image
    
################### SETUP
my_ip = "192.168.1.5"
his_ip = "192.168.1.6"
port = 2124

s = socket.socket()
s.bind((my_ip,port))
s.connect((his_ip, port))

camera = PiCamera()
rawCapture = PiRGBArray(camera)

################### Main
frame = captureFrame()
s.sendall(frame)


s.close()
s.detach()
