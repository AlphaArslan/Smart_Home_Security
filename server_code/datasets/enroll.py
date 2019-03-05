from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os

# managing argument parser for the script
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True, 
		help="path to where the face cascade resides")
ap.add_argument("-o", "--output", required=True,
		help="path to output directory")
args = vars(ap.parse_args())

# load OpenCV's Haar cascade for face detection from disk
detector = cv2.CascadeClassifier(args["cascade"])

# initialize the video stream, allow the camera sensor to warm up,
# and initialize the total number of example faces written to disk
# thus far
print("[INFO] starting video stream...")

#uncomment the coming line if using a pc
vs = VideoStream(src=0).start()

#uncomment the coming line if using Raspberry Pi
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
total = 0

while True:
	#capturing a frame and resizing it
	frame = vs.read()		#original frame
	orig = frame.copy()		#copy of that frame
	frame = imutils.resize(frame , width=400)

	#detect faces on gray frames [rectangles]
	rects =detector.detectMultiScale(
		cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1,
		minNeighbors= 5, minSize=(30,30) )

	#drawing rectangles over faces
	for (x,y,w,h) in rects:
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

	#display
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	#press 'k' to save the frame as a dataset image
	if key == ord("k"):
		p = os.path.sep.join([args["output"], "{}.png".format(
			str(total).zfill(5))])
		cv2.imwrite(p, orig)
		total += 1

	#press 'q' to end the process
	elif key == ord("q"):
		break

# print the total faces saved and do a bit of cleanup
print("[INFO] {} face images stored".format(total))
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()

