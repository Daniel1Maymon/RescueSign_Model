# This is client code to receive video frames over UDP
import cv2
import socket
import time
import pickle
import random
import os

BUFF_SIZE = 65536
HEADERSIZE = 10

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

host_name = socket.gethostname()
host_ip = '0.0.0.0'
port = 9999
socket_address = (host_ip, port)

message = b'Hello from client'

client_socket.sendto(message, socket_address)
fps, st, frames_to_count, cnt = (0, 0, 20, 0)
path_out = '/root/Environments/python-send-video-with-socket/client-frames/'
count = 0

while True:
    packet, _ = client_socket.recvfrom(BUFF_SIZE)
    # npdata = pickle.loads(packet[HEADERSIZE:])
    
    id, encoded_frame = pickle.loads(packet[HEADERSIZE:])
    # decoded_frame = cv2.imdecode(encoded_frame, 1)
    # decoded_frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)

    # buffer_id = id_and_buffer[0]
    # response = (buffer_id, random.choice(["YES", "NO"]))
    model_answer = random.choice(["YES", "NO"])
    response = (encoded_frame, id, model_answer)
    encoded_response = pickle.dumps(response)

    print(f"id = {id}")

    # client_socket.sendto(pickle.dumps(response), socket_address)
    client_socket.sendto(encoded_response, socket_address)
    
    decoded_frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)
    frame = cv2.putText(decoded_frame, 'FPS:' + str(fps),
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow('RECEIVING VIDEO', frame)

    full_path = os.path.join(path_out, id)
    cv2.imwrite(full_path + ".jpg", frame)
    # cv2.imwrite(path_out + "frame%d.jpg" % count, encoded_frame)
    count +=1

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
        break
    if cnt == frames_to_count:
        try:
                fps = round(frames_to_count/(time.time()-st))
                st=time.time()
                cnt = 0
        except:
                pass
    cnt +=1