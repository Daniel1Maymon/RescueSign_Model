from flask_socketio import SocketIO, emit
import json
import os
import cv2
import imutils
import pickle
import socket
import datetime
import time

BUFF_SIZE = 65536
HEADERSIZE = 10

class ModelSocket:
    def __init__(self, video_name):
        self.video_name = video_name

    def get_src_vid_path(self):
        self.file_path = os.path.abspath(__file__)

        # Get the directory name of the current file
        self.dir_name = os.path.dirname(self.file_path)

        self.videos_location = f'{self.dir_name}/static'

        self.path_out = f'{self.dir_name}/static/model-server-frames'

        return self.path_out, self.videos_location

    def create_socket_and_bind_it(self):
        HOST = '127.0.0.1'  # the IP address of the operator server
        PORT = 5001  # the port number used by the operator server

        self.model_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.model_server_socket.setsockopt(
        socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

        # Bind the socket to a specific address and port
        socket_address = (HOST, PORT)
        self.model_server_socket.bind(socket_address)

        print(f"Listening at: {socket_address}")
        print('Waiting for operator server connection...')

        msg, self.client_addr = self.model_server_socket.recvfrom(BUFF_SIZE)

        # Receive data from the operator server
        print('Data received from Operator server: ', msg.decode())

        # return model_server_socket, client_addr

    # send_video_frames(model_server_socket, client_addr)
    # def send_video_frames(sock, client_addr)
    def send_video_frames(self):
    
        # Get the full path of the current file
        path_out, dir_name = self.get_src_vid_path()
        video_src = f'{dir_name}/{self.video_name}'

        # Open the video file or capture from a camera
        vid = cv2.VideoCapture(video_src)

        frame_rate = 6  # Desired frame rate (6 frames per second)
        frame_interval = 1 / frame_rate  # Interval between frames
        start_time = time.time()  # Update start time

        while vid.isOpened():
            # start_time = time.time()  # Initialize start time
            return_val, frame = vid.read()
            if not return_val:
                id_and_frame = ('FINISH', None)
                message = pickle.dumps(id_and_frame)
                message = bytes(f'{len(message): < {HEADERSIZE}}', "utf-8") + message
                self.model_server_socket.sendto(message, self.client_addr)

                print("Close the socket connection")
                self.model_server_socket.close()
                break

            # Calculate the elapsed time since the last frame
            elapsed_time = time.time() - start_time

            # If the elapsed time is greater than the frame interval, send the frame
            if elapsed_time >= frame_interval:
                # ... (send the frame)
                WIDTH = 400
                frame = imutils.resize(frame, width=WIDTH)

                buffer_id = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
                full_path = os.path.join(path_out, buffer_id)

                print(f"buffer_id = {buffer_id}")

                # Save the frame as image:
                cv2.imwrite(path_out + ".jpg", frame)

                # Encode the frame:
                encoded_succes, encoded_frame = cv2.imencode(
                    '.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

                # Serialize the frame into a byte array
                id_and_frame = (buffer_id, encoded_frame)
                message = pickle.dumps(id_and_frame)
                # frame_data = pickle.dumps(encoded_frame)

                # message = pickle.dumps(frame_data)
                message = bytes(
                    f'{len(message): < {HEADERSIZE}}', "utf-8") + message
                self.model_server_socket.sendto(message, self.client_addr)

                #############################################
                start_time = time.time()  # Update the start time



        # Release the video capture
        vid.release()

