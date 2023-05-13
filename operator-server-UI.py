from flask import Flask, render_template, request 
import requests
from auxiliary_functions import read_all_frames, frames_to_video


app = Flask(__name__)

def read_frames() -> list:
    
    return []

@app.route('/')
def index():
    framePaths = read_all_frames()
    mp4_path = frames_to_video(framePaths)

    file_path1 = '/root/Environments/rescueSign/static/output.mp4'
    file_path2 = '/root/Environments/rescueSign/static/kitty.mp4'
    import magic
    video_type1 = magic.from_file(file_path1, mime=True)
    video_type2 = magic.from_file(file_path2, mime=True)
    print(f"video_type1 = {video_type1}")
    print(f"video_type2 = {video_type2}")

    # Render the HTML template with frames and options for the operator
    return render_template('display.html', video_path=mp4_path, mimetype='video/mp4')


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
