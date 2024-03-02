import os
# from flask_socketio import SocketIO
import json
import os
import cv2
import imutils
import pickle
import socket
import datetime
import time
import auxiliary_functions
import math

BUFF_SIZE = 65536
HEADERSIZE = 10

class ModelSocket:
    
    def __init__(self, video_name):
        print("(step 1) :: ModelSocket :: __init__ ")
        self.video_name = video_name

        # TODO: Create Model
        # from Rescue_Sign import RescueSignModel
        # self.model = RescueSignModel()

    def get_src_vid_path(self):
        self.file_path = os.path.abspath(__file__)

        # Get the directory name of the current file
        self.dir_name = os.path.dirname(self.file_path)

        # For ubuntu:
        # self.videos_location = f'{self.dir_name}/static'
        # self.path_out = f'{self.dir_name}/static/model-server-frames'

        # For windows:
        self.videos_location = self.dir_name + '\static'
        self.path_out = self.dir_name + '\static\model-server-frames'


        # return self.path_out, self.videos_location

    def open_operator_socket(self):
        print("::: open_operator_socket() ::::")
        import requests
        url = "http://127.0.0.1:5050/create_socket_connection"

        headers = {
            'Content-Type': 'application/json'
        }

        # Send a GET request:
        response = requests.get(url, headers=headers)

        # Check the response status code
        if response.status_code == 200:  # 200 indicates a successful request
            # Access the response content
            data = response.json()  # Assuming the response is in JSON format
            # Process the data or perform further operations
            print(data)
        else:
            print("GET request failed with status code:", response.status_code)

    def create_socket_and_bind_it(self):
        HOST = '127.0.0.1'  #  the server will listen for connections on the same machine.
        PORT = 4001  # The port number 4001 is assigned to the server.

        # self.open_operator_socket()

        # socket.socket() - A socket object is created.
        # socket.AF_INET - specifying the address family as AF_INET (IPv4)
        # socket.SOCK_DGRAM - specifying the socket type as SOCK_DGRAM (UDP socket)
        self.model_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        
        #  setsockopt() - set the socket's receive buffer size.
        # SOL_SOCKET (socket-level option)
        # SO_RCVBUF (receive buffer size).
        self.model_server_socket.setsockopt(
        socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

        # Bind the socket to a specific address and port
        socket_address = (HOST, PORT)
        self.model_server_socket.bind(socket_address)

        print(f"Listening at: {socket_address}")
        print('Waiting for operator server connection...')

        msg, self.client_addr = self.model_server_socket.recvfrom(BUFF_SIZE)

        # Receive data from the operator server
        # print('Data received from Operator server: ', msg.decode())

        # return model_server_socket, client_addr

    def send_frames_by_chunks(self):
        print(":: send_frames_by_chunks ::")
        
        '''
        1. Save the full video path
        2. Open the video file with CV2
        3. Read and save the video frames:
            3.1. Save every sixth frame in chunk
            3.2. When the chunk is filled with 50 frames, we will send the chunk to the operator (using socket)
        '''
        
        pendingImages_folder = 'C:\\Users\\project25\\RescueSign\\PendingImages'
        
        # Get the full path of the current file
        # _, static_folder_location = self.get_src_vid_path()
        
        self.get_src_vid_path()
        video_full_path = self.dir_name + "/static/" + self.video_name

        # Open the video file or capture from a camera
        vid = cv2.VideoCapture(video_full_path)

        
        # initialize frame_counter:
        frames_counter = 0
        frame_index = 0
        chunk_size = 50
        frames_chunk = []
        fps = 6  # Desired frame rate (6 frames per second)
        
        
        vid_frame_rate = vid.get(cv2.CAP_PROP_FPS)
        time1 = time.time()
        
        # total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        # print(f"total frames = {total_frames}")

        while vid.isOpened():
            return_val, frame = vid.read()
            # After reading the last frame:
            if not return_val:
                # If the current chunk contains frames, send the frames
                # self.process_remaining_frames(frames_chunk)
                self.process_frames_chunk(frames_chunk)
                break


            '''
            Save every sixth frame in the current chunk::
            ''' 
            frame_position = vid.get(cv2.CAP_PROP_POS_FRAMES)
            frame_is_needed = self.is_frame_needed(frame_position, vid_frame_rate, fps) # True/False - Check if the frame need to be check
            
            if frame_is_needed:
                frame_and_id = self.save_frame(frame, pendingImages_folder)
                frames_chunk.append(frame_and_id)
                frames_counter += 1

            # When the current chunk contains chunk_size, send the chunk
            if frames_counter >= chunk_size:
                self.process_frames_chunk(frames_chunk)
                frames_chunk = []
                frames_counter = 0
            frame_index += 1
        
        # Release the video capture
        vid.release()
        time2 = time.time()
        print(f"::: Total running time: {time2 - time1}")

    def save_frame(self, frame, pendingImages_folder):
        return self.save_frame_on_disk(frame, pendingImages_folder)
    
    def process_frames_chunk(self, frames_chunk):
        '''
        Model version:
        '''
        # try:
        #     # TODO: run model
        #     print("Model is running...")
        #     print("Sending chunk...")
        #     # self.model.run_model()
        #     # if len(self.model.output) > 0:
        #     #     self.create_socket_and_bind_it()
        #     #     self.send_frames_to_operator(frames_chunk, self.model.output)
        # except Exception as e:
        #     print("An exception occured: ", str(e))
        
        '''
        No Model version:
        '''
        if frames_chunk:
            self.create_socket_and_bind_it()
            self.send_frames_to_operator(frames_chunk)
            
            
        print("Delete the frames from disk...")
        # auxiliary_functions.delete_files_in_directory(folder_name="PendingImages")
    
    def process_remaining_frames(self, frames_chunk):
        print("::: process_remaining_frames() :::")
        try:
            # self.model.run_model()
            print("run model ")
            print("TODO: if the model detacts frames with rescue sign, send the frames to Operator")
            # if len(self.model.output) > 0:
            #     self.create_socket_and_bind_it()
            #     self.send_frames_to_operator(frames_chunk, self.model.output)
        except Exception as e:
            print("An exception occured: ", str(e))
            
        print("Delete the frames from disk...")
        # auxiliary_functions.delete_files_in_directory(folder_name="PendingImages")
        
    def is_frame_needed(self, frame_position, vid_frame_rate, fps):
        res = frame_position % math.ceil(vid_frame_rate / fps) == 0
        return res



    def send_frames_to_operator(self, frames_chunk):
        
        for frame, frame_id in frames_chunk:
            # Encode the frame:
            WIDTH = 400
            frame = imutils.resize(frame, width=WIDTH)
            print(f"frame_id = {frame_id}")
            encoded_succes, encoded_frame = cv2.imencode(
            '.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

            # Serialize the frame (into a byte array) with pickle 
            id_and_frame = (frame_id, encoded_frame)
            message = pickle.dumps(id_and_frame) 

            message = bytes(f'{len(message): < {HEADERSIZE}}', "utf-8") + message
            self.model_server_socket.sendto(message, self.client_addr)

        # When all the frames have been sent, send empty message to operator
        id_and_frame = ('FINISH', None)
        message = pickle.dumps(id_and_frame)
        message = bytes(f'{len(message): < {HEADERSIZE}}', "utf-8") + message
        self.model_server_socket.sendto(message, self.client_addr)

        print("Close the socket connection")
        self.model_server_socket.close()
        pass
        
    '''
    Use only when model works
    '''
    # def send_frames_to_operator(self, frames_chunk, model_output_list):
        
    #     # frames_chunk = [(frame, id), (), ()]
    #     # frame_id = frame_and_id[1]

    #     model_output_list = [x.split(".")[0] for x in model_output_list]
    #     frames_chunk_to_send = [frame_and_id for frame_and_id in frames_chunk if frame_and_id[1] in model_output_list]

    #     # for x in frames_chunk:
    #     #     print(f':::frame_id = {x[1]} :::::')

    #     print(f"len(frames_chunk_to_send) = {len(frames_chunk_to_send)}")

    #     # for frame, frame_id in frames_chunk:
    #     for frame, frame_id in frames_chunk_to_send:
    #         # Encode the frame:
    #         WIDTH = 400
    #         frame = imutils.resize(frame, width=WIDTH)
    #         print(f"frame_id = {frame_id}")
    #         encoded_succes, encoded_frame = cv2.imencode(
    #         '.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

    #         # Serialize the frame into a byte array
    #         id_and_frame = (frame_id, encoded_frame)
    #         message = pickle.dumps(id_and_frame)

    #         message = bytes(f'{len(message): < {HEADERSIZE}}', "utf-8") + message
    #         self.model_server_socket.sendto(message, self.client_addr)

    #     id_and_frame = ('FINISH', None)
    #     message = pickle.dumps(id_and_frame)
    #     message = bytes(f'{len(message): < {HEADERSIZE}}', "utf-8") + message
    #     self.model_server_socket.sendto(message, self.client_addr)

    #     print("Close the socket connection")
    #     self.model_server_socket.close()

    def save_frame_on_disk(self, frame, dest):
        buffer_id = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        des_path = os.path.dirname(os.path.abspath(__file__)).replace("rescueSign", "rescueSign/modelFolders/PendingImages/")
        frame_dest = des_path + buffer_id + ".jpg"
        
        cv2.imwrite(frame_dest, frame)

        return (frame, buffer_id)

    def save_video_frames(self, video_name):
            print(":: save_video_frames :: ")
            # Get the full path of the current file
            _, static_folder_location = self.get_src_vid_path()
            pending_images_folder = 'C:\\Users\\project25\\RescueSign\\PendingImages'

            video_src = static_folder_location + "\\" + self.video_name
            print(f"video_src = {video_src}")

            # # Open the video file or capture from a camera
            vid = cv2.VideoCapture(video_src)

            total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"total frames = {total_frames}")

            current_frame = 0

            frame_rate = 6  # Desired frame rate (6 frames per second)
            frame_interval = 1 / frame_rate  # Interval between frames
            start_time = time.time()  # Update start time

            while vid.isOpened():
                return_val, frame = vid.read()
                if not return_val:
                    break

                # Calculate the elapsed time since the last frame
                elapsed_time = time.time() - start_time

                # If the elapsed time is greater than the frame interval, send the frame
                if elapsed_time >= frame_interval:
                    buffer_id = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
                    full_path = os.path.join(pending_images_folder, buffer_id) + ".jpg"


                    # Save the frame as image:
                    cv2.imwrite(full_path + ".jpg", frame)
                    


                    #############################################
                    start_time = time.time()  # Update the start time

                current_frame +=1
            # Release the video capture
            vid.release()

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



