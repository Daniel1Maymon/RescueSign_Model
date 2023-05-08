# This is server code to send video frames over UDP
import cv2, imutils, socket
import time
import pickle
import uuid
import os
import datetime
import numpy as np

BUFF_SIZE = 65536
HEADERSIZE = 10

server_socket = None
try:
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

    host_name = socket.gethostname()
    host_ip = '0.0.0.0'
    port = 9999

    socket_address = (host_ip, port)
    server_socket.bind(socket_address)

    print(f"Listening at: {socket_address}")

    count = 0

    # Get the full path of the current file
    file_path = os.path.abspath(__file__)

    # Get the directory name of the current file
    dir_name = os.path.dirname(file_path)

    path_out = f'{dir_name}/server-frames'
    video_src = f'{dir_name}/kitty.mp4'

    vid = cv2.VideoCapture(video_src)
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)

    while True:
        msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ', client_addr)
        print(f"msg = {msg.decode('utf-8')}")

        WIDTH = 600

        while vid.isOpened():
            _, frame = vid.read()
            if frame is not None:
                frame = imutils.resize(frame, width=WIDTH)
                buffer_id = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
                full_path = os.path.join(path_out, buffer_id)

                # Save the frame as image:
                cv2.imwrite(full_path + ".jpg", frame)
                '''
                cv2.imencode - used to encode an image in a specific format
                encoded_success - a boolean value that indicates whether the encoding was successful or not
                encoded_frame -  contains the encoded image data
                '''
                encoded_success, encoded_frame = cv2.imencode(
                    '.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                count += 1

                id_and_frame = (buffer_id, encoded_frame)
                message = pickle.dumps(id_and_frame)
                message = bytes(
                    f'{len(message): < {HEADERSIZE}}', "utf-8") + message
                server_socket.sendto(message, client_addr)

                response_from_client, client_addr = server_socket.recvfrom(
                    BUFF_SIZE)
                encoded_frame_from_client, frame_id, model_answer = pickle.loads(
                    response_from_client)
                decoded_frame_from_client = cv2.imdecode(
                    encoded_frame_from_client, cv2.IMREAD_COLOR)

                # img = cv2.imread(f'{path_out}{frame}.jpg')
            #     # Convert the image to a NumPy array with data type uint8
            #     # img_data = np.frombuffer(img.tobytes(), dtype=np.uint8)
                # frame = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
                frame = cv2.putText(decoded_frame_from_client,
                                    f'FPS: {str(fps)} :: {model_answer}',
                                    (10, 40),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.7,
                                    (0, 0, 255),
                                    2)
                cv2.imshow('TRANSMITTING_VIDEO', frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    server_socket.close()
                    break
                if cnt == frames_to_count:
                    try:
                        fps = round(frames_to_count/(time.time()-st))
                        st = time.time()
                        cnt = 0
                    except:
                        pass
                cnt += 1

            else:
                break
                vid = cv2.VideoCapture(video_src)
                fps, st, frames_to_count, cnt = (0, 0, 20, 0)
                count = 0
except socket.error as e:
    print(f"Socket error occurred: {e}")

