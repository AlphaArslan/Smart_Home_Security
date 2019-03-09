import face_recognition
import argparse
import pickle
import cv2
import numpy as np
import sys
import time

from Communication import *
from frameProcess  import *


# script arguments
ap = argparse.ArgumentParser()

ap.add_argument("-r", "--rpi", required=True,
		help="The address of Raspberry Pi from which we bring the stream")
ap.add_argument("-p", "--port", required=True,
		help="the port through which stream is being sent")
ap.add_argument("-e", "--encodings", required=True,
		help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
		help="face detection model to use: either `hog` or `cnn`")

args = vars(ap.parse_args())



# Setup
print("[INFO]:loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

cv2.namedWindow("Image")

# Create a UDP socket
host = args["rpi"]
port = int(args["port"])
sock = create_socket()
sock.settimeout(1)
internal_sock = create_socket()



if __name__ == '__main__':
	while True:
		frame = get_frames(host, port, sock)
		names , processed_frame = process_frame(frame, args["detection_method"], data)
		ret, jpeg = cv2.imencode('.jpg', processed_frame)
		frame_bytes = jpeg.tobytes()
		send_frame_bytes(frame_bytes, internal_sock, 4575)

# print("The client is quitting. If you wish to quite the server, simply call : \n")
# print("echo -n \"quit\" > /dev/udp/{}/{}".format(host, port))
