import os
import subprocess
import time
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    start_time = time.time()
    link = request.form['link']
    host = os.environ.get('SINGAPORE_IP')
    file_name = os.path.basename(link)
    current_time = time.strftime('%Y-%m-%d_%H:%M:%S')
    remote_folder = "/root/files/" + current_time
    create_folder_command = f"mkdir -p {remote_folder}"
    subprocess.run(f"ssh root@{host} '{create_folder_command}'", shell=True)
    file_path = os.path.join(remote_folder, file_name)

    with requests.get(link, stream=True) as r:
        r.raise_for_status()
        with subprocess.Popen(f"ssh root@{host} 'cat > {file_path}'", shell=True, stdin=subprocess.PIPE) as p:
            for chunk in r.iter_content(chunk_size=8192):
                p.stdin.write(chunk)
    end_time = time.time()
    time_spent = round(end_time - start_time, 3)
    return render_template('upload_success.html',
                           filename=file_name, time_spent=time_spent, download_link="")


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
    app.run(debug=True, host='localhost')
