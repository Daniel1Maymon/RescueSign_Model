from flask import Flask, render_template, request, jsonify
import requests
from auxiliary_functions import read_all_frames, delete_files_in_directory
from operator_socket_class import OperatorSocket

app = Flask(__name__)

@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/')
def index():

    framePaths = read_all_frames() 
    return render_template('display.html', imageUrls=framePaths)
    # return render_template('display.html')

def send_answer(selected_answer):
    # Process the selected answer
    print("Selected answer:", selected_answer)    

@app.route('/get_images_urls')
def get_images_urls():
    framePaths = read_all_frames() 
    return jsonify(framePaths)

@app.route('/create_socket_connection')
def create_socket_connection():
    # First, delete all the oldest frames
    delete_files_in_directory()


    # open socket connection
    opertor_socket = OperatorSocket()
    opertor_socket.create_socket_and_bind_it_to_model()
    opertor_socket.get_frames_from_model_server()

    print('Video frames have been send')

    return 'Success'

@app.route('/delete_oldest_frames')
def delete_oldest_frames():
    # First, delete all the oldest frames
    delete_files_in_directory()

    return jsonify("{'message': 'Oldest frames have been deleted'}")

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    selected_answer = request.form['answer']
    send_answer(selected_answer)
    
    return 'Success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
