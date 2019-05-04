import socket
import cv2
import numpy as np

def create_socket():
	# Create a UDP socket
	print("[INFO]:Creating Socket... ")
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return sock

def create_socket_receiving(port, host="127.0.0.1"):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((host, port))
	return sock

def get_frames(host, port, sock):
	print("[INFO]:Sending GET request...")
	sent = sock.sendto("get".encode('ascii'), (host, port))

	try:
		answer, server = sock.recvfrom(65507)
	except socket.timeout :
		return get_frames(host, port, sock)

	print("[INFO]:Frame Received")

	array = np.frombuffer(answer, dtype=np.dtype('uint8'))
	frame = cv2.imdecode(array, 1)

	return frame

def get_frames_base64(host, port, sock):
	print("[INFO]:Sending BASE request...")
	sent = sock.sendto("base".encode('ascii'), (host, port))

	try:
		answer, server = sock.recvfrom(65507)
	except socket.timeout :
		return get_frames_base64(host, port, sock)

	print("[INFO]:Frame Received")
	return answer


def send_frame_bytes(frame_bytes, sock, port):
	sock.sendto(frame_bytes, ("127.0.0.1", port))
