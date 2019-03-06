import face_recognition
import cv2
import numpy as np
import sys
import time


def process_frame(frame, detection_method, data):
	#face Recognition starts here
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	#detecting faces and calculating encodings
	print("[INFO]:recognizing faces...")
	boxes = face_recognition.face_locations(rgb,
		model=detection_method)
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
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)
	return frame
