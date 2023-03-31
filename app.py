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
    return render_template('upload_success.html',
                           filename=filename, time_spent=time_spent, download_link=download_link)


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
