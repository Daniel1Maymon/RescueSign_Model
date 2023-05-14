from flask import Flask, render_template, request 
import requests
from auxiliary_functions import read_all_frames


app = Flask(__name__)

def read_frames() -> list:
    
    return []

@app.route('/')
def index():
    framePaths = read_all_frames()
    return render_template('display.html', imageUrls=framePaths)


@app.route('/send_answer', methods=['POST'])
def send_answer():
    # Get the selected answer from the form submission
    selected_answer = request.form['answer']

    # send the selected answer to the Model server via HTTP POST request
    model_server_url = ''
    json = {'answer': selected_answer}
    response  = requests.post(model_server_url, json=json)

    return render_template('operator.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
