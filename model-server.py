from flask_socketio import SocketIO, emit
import json
import os
import cv2
import imutils
import pickle
import socket
import datetime

BUFF_SIZE = 65536
HEADERSIZE = 10

def receive_message_from_operator(ws):
    message = ws.recv()
    data = json.loads(message)

    # Handle the received data
    if 'action' in data:
        if data['action'] == 'emergency_signal':
            # Send an HTTP request or signal to trigger the drone's siren
            # active_emerg_signal_in_drone()
            print('Active emergany signal in drone')


def on_error(ws, error):
    # Handle any errors that occur during the WebSocket connection
    pass


def get_src_vid_path():
    file_path = os.path.abspath(__file__)

    # Get the directory name of the current file
    dir_name = os.path.dirname(file_path)
    path_out = f'{dir_name}/model-server-frames'

    return path_out, dir_name


def send_video_frames(sock, client_addr):

    # Get the full path of the current file
    path_out, dir_name = get_src_vid_path()
    video_src = f'{dir_name}/kitty.mp4'

    # Open the video file or capture from a camera
    vid = cv2.VideoCapture(video_src)

    while vid.isOpened():
        return_val, frame = vid.read()
        if not return_val:
            id_and_frame = ('FINISH', None)
            message = pickle.dumps(id_and_frame)
            message = bytes(f'{len(message): < {HEADERSIZE}}', "utf-8") + message
            sock.sendto(message, client_addr)

            print("Close the socket connection")
            model_server_socket.close()
            break

        WIDTH = 600
        frame = imutils.resize(frame, width=WIDTH)

        buffer_id = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        full_path = os.path.join(path_out, buffer_id)

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
        sock.sendto(message, client_addr)



    # Release the video capture
    vid.release()


# Start sending video frames
# send_video_frames()

def create_socket_and_bind_it():
        HOST = '127.0.0.1'  # the IP address of the operator server
        PORT = 5001  # the port number used by the operator server

        model_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        model_server_socket.setsockopt(
        socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

        # Bind the socket to a specific address and port
        socket_address = (HOST, PORT)
        model_server_socket.bind(socket_address)

        print(f"Listening at: {socket_address}")
        print('Waiting for operator server connection...')

        msg, client_addr = model_server_socket.recvfrom(BUFF_SIZE)

        # Receive data from the operator server
        print('Data received from Operator server: ', msg.decode())

        return model_server_socket, client_addr

if __name__ == '__main__':
    # Create a socket object for connection with the operator server and bind it 
    model_server_socket, client_addr = create_socket_and_bind_it()

    send_video_frames(model_server_socket, client_addr)

    # # Send the response back to the operator server
    # conn.sendall(response)


