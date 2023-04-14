import os
import subprocess
import io
import time

from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file, Response, url_for

from file_handler_processor import FileProcessor
from location_resolver import LocationResolver

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download_success')
def download_success():
    download_time_ms = request.args.get('download_time')
    download_time_sec = round(int(download_time_ms) / 1000, 2)
    file_location = LocationResolver().get_droplet_location(request)

    return render_template('download_success.html',
                           download_time=download_time_sec,
                           file_ip=file_location[1],
                           file_vps=file_location[0],
                           current_time=time.strftime('%Y-%m-%d %H:%M:%S'))


@app.route('/upload', methods=['POST'])
def upload():
    link = request.form['link']

    droplet_location, droplet_ip = LocationResolver().get_droplet_location(link)

    file_handler_processor = FileProcessor()
    upload_data = file_handler_processor.upload_file_by_link(link=link, droplet_ip=droplet_ip)
    upload_data.update({"host_name": droplet_location,
                        "vps_num": droplet_location.split(" ")[0]})

    sync_data = file_handler_processor.sync_uploaded_file(droplet_ip=droplet_ip)

    return render_template('upload_success.html',
                           upload_data=upload_data,
                           sync_data=sync_data,
                           download_url=os.environ.get("DOWNLOAD_URL"))


@app.route('/download_file/<path:file_path>')
def download_file(file_path):
    droplet_ip = LocationResolver().get_droplet_location(request)[1]
    execution_command = FileProcessor().get_file_download_command(droplet_ip=droplet_ip, file_path=file_path)
    file_name = os.path.basename(file_path)
    with subprocess.Popen(execution_command, shell=True, stdout=subprocess.PIPE) as p:
        buffer = io.BytesIO(p.stdout.read())
    return send_file(buffer, as_attachment=True, download_name=file_name)


if __name__ == '__main__':
    app.run(debug=True, host='localhost')
