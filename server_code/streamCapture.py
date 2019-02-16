################### IMPORT
import socket
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

################### Function
def getprivatekey():
    privateKey = tuple(map(int,input("Enter publicKey q, n : ").split(',')))
    return privateKey

def RSA_decrypt(text)
	return text

################### Setup
my_ip  = "192.168.1.6"
his_ip = "192.168.1.5"
port   = 2124

s = socket.socket()
s.bind((my_ip, port))
s.listen(1)
conn, addr = s.accept()
print "connected to : ", addr

rawCapture = PiRGBArray(camera)
################### Main

rawCapture = conn.recv(50000)
image = rawCapture.array

cv2.imshow("Image", image)
cv2.waitKey(0)

conn.close()
