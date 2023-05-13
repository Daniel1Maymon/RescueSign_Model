from flask import Flask, render_template, redirect, url_for
import socket
import pickle
import cv2
import os

BUFF_SIZE = 65536
HEADERSIZE = 10
HOST = '127.0.0.1'  # the IP address of the model server
PORT = 5001  # the port number used by the model server
fps, st, frames_to_count, cnt = (0, 0, 20, 0)

app = Flask(__name__)
# socketio = SocketIO(app)

#  Set up the routes for the operator server endpoints
@app.route('/')
def index():
    return render_template('index.html')



# Get the full path of the current file
file_path = os.path.abspath(__file__)

# Get the directory name of the current file
dir_name = os.path.dirname(file_path)
path_out = f'{dir_name}/operator-server-frames/'


def create_socket_and_bind_it() -> socket.socket:
    print("Operator server create a socket object for connection with the model server")
    socket_address = (HOST, PORT)

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

    # Bind the socket to a specific address and port
    # sock.bind(socket_address)

    # Send data to the model server
    data = b'Hello from operator server'
    sock.sendto(data, socket_address)
    return sock


@app.route('/display')
def display_frames(frames):
    return render_template('display.html', frames=frames)

def get_frames_from_model_server(sock: socket.socket) -> list:
    while True:
        # Receive response from the model server
        packet, _ = sock.recvfrom(BUFF_SIZE)
        frame_id, encoded_frame = pickle.loads(packet[HEADERSIZE:])

        if 'FINISH' in frame_id:
            print("Close the socket connection")
            sock.close()
            print(f"len(frames = {len(frames)})")
            return frames

        decoded_frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)
        frame = cv2.putText(decoded_frame, 'FPS:' + str(fps),
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 0, 255),
                            2)
        full_path = os.path.join(path_out, frame_id)
        cv2.imwrite(full_path + ".jpg", frame)

        frames.append(frame)


def trigger_the_disaply_page(frames):
    # Trigger the redirect to the '/display' route
    return redirect(url_for('display'))

if __name__ == '__main__':

    # Create a socket object for connection with the operator server and bind it
    sock = create_socket_and_bind_it()


    
    frames = []  # List to store received frames
    frames = get_frames_from_model_server(sock)

    # After all frames have been received
    app.run(host=HOST, port=PORT)
    trigger_the_disaply_page(frames)


        