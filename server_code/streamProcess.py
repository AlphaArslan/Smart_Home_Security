#!/usr/bin/env python
# coding: utf-8

import face_recognition
import argparse
import pickle
import socket
import cv2
import numpy as np
import sys
import time

#script arguments
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

print("[INFO]:loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())


cv2.namedWindow("Image")

# Create a UDP socket
print("[INFO]:Creating Socket... ")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = args["rpi"]
port = int(args["port"])
server_address = (host, port)

while(True):
	print("[INFO]:Sending GET request...")
	sent = sock.sendto("get".encode('ascii'), server_address)

	answer, server = sock.recvfrom(65507)
	#print("Fragment size : {}".format(len(data)))
	print("[INFO]:Frame Received")

	if len(answer) == 4:
		# This is a message error sent back by the server
		if(answer == "FAIL"):
			continue

	array = np.frombuffer(answer, dtype=np.dtype('uint8'))
	image = cv2.imdecode(array, 1)

	#face Recognition starts here
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	#detecting faces and calculating encodings
	print("[INFO]:recognizing faces...")
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])
	encodings = face_recognition.face_encodings(rgb, boxes)

	names = []

	#loop over faces and comparing to known faces
	for encoding in encodings:
		matches = face_recognition.compare_faces(data["encodings"],encoding)
		name = "Unknown"

		#matches contains True for every match and False for every dismatch
		#we now compute what name got the most Trues "votes"
		if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number of
			# votes (note: in the event of an unlikely tie Python will
			# select first entry in the dictionary)
			name = max(counts, key=counts.get)

		# update the list of names
		names.append(name)


	# loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# draw the predicted face name on the image
		cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)


	cv2.imshow("Image", image)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

print("The client is quitting. If you wish to quite the server, simply call : \n")
print("echo -n \"quit\" > /dev/udp/{}/{}".format(host, port))
