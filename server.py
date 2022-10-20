from operator import truediv
import struct

import socket
import pickle
import threading
import cv2

PORT = 25565
IP = socket.gethostbyname(socket.gethostname())

print(f'Server started on port {PORT} with IP {IP}.')
running = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))

def handle_request(conn, addr):
    print(f'{addr} conected on port {PORT}.')
    connected = True

    if conn:
        print("HELLO WORLD")
        vid = cv2.VideoCapture(0)
        
        while vid.isOpened():
            img, frame = vid.read()
            video = pickle.dumps(frame)
            msg = struct.pack('Q', len(video))
            conn.sendall(msg)

            cv2.imshow(f'Transmitting from {IP}:{PORT}', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                conn.close()

def start_server():
    server.listen()

    print(f'Server active on port {PORT} with IP {IP}')

    while running:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_request, args=(conn, addr))
        thread.start()
        print(f'{threading.active_count() - 1} users are currently connected')

start_server()