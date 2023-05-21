from flask import Flask, render_template, request 
import requests
from auxiliary_functions import read_all_frames


app = Flask(__name__)

@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/')
def index():
    framePaths = read_all_frames()
    return render_template('display.html', imageUrls=framePaths)

def send_answer(selected_answer):
    # Process the selected answer
    print("Selected answer:", selected_answer)    

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    selected_answer = request.form['answer']
    send_answer(selected_answer)
    return 'Success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
