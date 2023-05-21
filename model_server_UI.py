from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)

@app.route('/response_from_operator', methods=['POST'])
def get_response():
    data = request.json

    print(f'operator response: {data}')

    return 'POST request received'

@app.route('/model_ui', methods=['GET'])
def model_ui():
    return render_template('model_ui.html')

@app.route('/get_file_names')
def get_file_names():
    # Get the full path of the current file
    file_path = os.path.abspath(__file__)
    # Get the directory name of the current file
    dir_path = os.path.dirname(file_path) + '/static'

    file_names = [file for file in os.listdir(dir_path) if '.mp4' in file]

    return jsonify(file_names)

@app.route('/process_file', methods=['POST'])
def process_file():
    data = request.get_json()
    selected_option = data['option']



    return 'Option received'

# @app.route('/')
# def index():
#     return render_template('main_model_UI.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4002)