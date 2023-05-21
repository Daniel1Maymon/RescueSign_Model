import os
from model_server_socket import create_socket_and_bind_it, send_video_frames
from operator_server_socket import create_socket_and_bind_it_to_model

def read_all_frames():
    frames = []
    # Get the full path of the current file
    file_path = os.path.abspath(__file__)

    # Get the directory name of the current file
    dir_name = os.path.dirname(file_path)
    directory = f'{dir_name}/static/operator-server-frames/'

    # Get the list of files in the directory
    file_list = os.listdir(directory)

    # Filter out JPEG files
    jpeg_files = [file for file in file_list if file.endswith('.jpg')]
    jpeg_files.sort()
    jpeg_files = [os.path.join(
        'static/operator-server-frames/', file_name) for file_name in jpeg_files]

    # Read each JPEG file
    # for file_name in jpeg_files:
    #     file_path = os.path.join(directory, file_name)
    #     file_name = file_path
        # frame = cv2.imread(file_path)
        # frames.append(frame)
    
    return jpeg_files


async def send_video_from_model_to_operator():
    model_server_socket, client_addr = create_socket_and_bind_it()
    send_video_frames(model_server_socket, client_addr)

async def open_socket_in_model_side():
    sock = create_socket_and_bind_it_to_model()


    



