import subprocess
import glob
import os
import cv2

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


    



