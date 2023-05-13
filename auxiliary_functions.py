import glob
import os
import cv2

def read_all_frames():
    frames = []
    # Get the full path of the current file
    file_path = os.path.abspath(__file__)

    # Get the directory name of the current file
    dir_name = os.path.dirname(file_path)
    directory = f'{dir_name}/operator-server-frames/'

    # Get the list of files in the directory
    file_list = os.listdir(directory)

    # Filter out JPEG files
    jpeg_files = [file for file in file_list if file.endswith('.jpg')]
    jpeg_files.sort()
    jpeg_files = [os.path.join(directory, file_name) for file_name in jpeg_files]

    # Read each JPEG file
    # for file_name in jpeg_files:
    #     file_path = os.path.join(directory, file_name)
    #     file_name = file_path
        # frame = cv2.imread(file_path)
        # frames.append(frame)
    
    return jpeg_files


def frames_to_video(frame_paths):
    output_file = "output.mp4"

    # Get the first frame to obtain dimensions
    first_frame = cv2.imread(frame_paths[0])
    height, width, _ = first_frame.shape

    # Define the video codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_file, fourcc, 24, (width, height))

    # Write each frame to the video file
    for frame_path in frame_paths:
        frame = cv2.imread(frame_path)
        video_writer.write(frame)

    # Release the VideoWriter and close the video file
    video_writer.release()

    print(f"Video saved to: {output_file}")
    return output_file
    



