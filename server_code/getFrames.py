import socket
import cv2
import numpy as np

def create_socket():
	# Create a UDP socket
	print("[INFO]:Creating Socket... ")
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return sock


def get_frames(host, port, sock):
	print("[INFO]:Sending GET request...")
	sent = sock.sendto("get".encode('ascii'), (host, port))

	answer, server = sock.recvfrom(65507)
	#print("Fragment size : {}".format(len(data)))
	print("[INFO]:Frame Received")

	array = np.frombuffer(answer, dtype=np.dtype('uint8'))
	frame = cv2.imdecode(array, 1)

	return frame
