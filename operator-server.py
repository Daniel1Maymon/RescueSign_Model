from flask import Flask, render_template
import socket
import pickle
import cv2
import os

app = Flask(__name__)
# socketio = SocketIO(app)

#  Set up the routes for the operator server endpoints
@app.route('/')
def index():
    return render_template('index.html')


#  event handlers to handle websocket connections and messages
# @socketio.on('connect')
# def handle_connect():
#     print('Operator connected')
    # Additional initialization or setup code


# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Operator disconnected')
    # Clean-up code if needed

# @socketio.on('operator_input')
# def handle_operator_input(data):
#     # Process operator input and take action
#     # Send HTTP request or signal to the model server

#     # Example: Send a message back to the model server
#     emit('message_to_model', 'Emergency signal activated')

PORT = 5000
BUFF_SIZE = 65536
HEADERSIZE = 10
fps, st, frames_to_count, cnt = (0, 0, 20, 0)

# Get the full path of the current file
file_path = os.path.abspath(__file__)

# Get the directory name of the current file
dir_name = os.path.dirname(file_path)
path_out = f'{dir_name}/operator-server-frames/'

if __name__ == '__main__':
    # socketio.run(app, port=PORT)
    HOST = '127.0.0.1'  # the IP address of the model server
    PORT = 5001  # the port number used by the model server
    socket_address = (HOST, PORT)

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)


    # Send data to the model server
    data = b'Hello from operator server'
    sock.sendto(data, socket_address)

    frames = []  # List to store received frames

    while True:
        # Receive response from the model server
        packet, _ = sock.recvfrom(BUFF_SIZE)
        id, encoded_frame = pickle.loads(packet[HEADERSIZE:])

        if 'FINISH' in id:
            # display_frames()
            break

        decoded_frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)
        frame = cv2.putText(decoded_frame, 'FPS:' + str(fps),
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 0, 255),
                            2)
        full_path = path_out
        cv2.imwrite(full_path + ".jpg", frame)

        frames.append(frame)
        
        # print('Response from model server:', response.decode())

        # Close the socket connection
        sock.close()
        # print(f"Operator server is listening on {PORT}")
