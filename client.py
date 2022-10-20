import struct

import socket
import pickle
import cv2

PORT = 25565
IP = socket.gethostbyname(socket.gethostname())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
data = b''
payload = struct.calcsize('Q')

while True:
    while len(data) < payload:
        packet = client.recv(4096)
        if not packet: break
        data += packet
    
    msg_length = data[:payload]
    data = data[payload:]
    
    length = struct.unpack('Q', msg_length)[0]

    while len(data) < length:
        data += client.recv(4096)
    
    framedata = data[:length]
    data = data[length:]
    
    frame = pickle.loads(framedata)

    cv2.imshow('Video feed active', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

client.close()