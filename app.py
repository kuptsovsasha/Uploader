import os
import time
from flask import Flask, render_template, request, send_file

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    start_time = time.time()
    file = request.files['file']
    current_time = time.strftime('%Y-%m-%d_%H:%M:%S')
    folder_name = os.path.join('uploads', current_time)
    os.makedirs(folder_name) # create a new folder based on the current time
    filename = file.filename

    file.save(os.path.join(folder_name, filename))
    end_time = time.time()
    time_spent = end_time - start_time

    download_link = f'http://206.189.83.222:5000/download_file/{current_time}/{filename}'
    return f'''
    <!doctype html>
    <h1>The file {filename} was uploaded successfully.</h1>
    <h2>It took {time_spent} seconds to upload the file.</h2>
    <h2>You can download the file with link below:</h2>
    <a href="{download_link}">{download_link}</a>
    '''


@app.route('/download_file/<path:file_path>')
def download_file(file_path):
    print(file_path)
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    file_path = os.path.join(uploads_dir, file_path)
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return f"The requested file '{file_path}' does not exist."


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
