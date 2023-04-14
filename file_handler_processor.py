import os
import subprocess
import time

import requests


class FileProcessor:
    def __init__(self):
        self.file_folder = "/root/files/"
        self.droplets = [
            (os.environ.get('NEW_YORK_IP'), "VPS2 New York"),
            (os.environ.get('SINGAPORE_IP'), "VPS3 Singapore"),
            (os.environ.get('FRANKFURT_IP'), "VPS1 Frankfurt")
        ]

    def upload_file_by_link(self, link: str, droplet_ip: str) -> dict:
        start_time = time.time()
        file_name = os.path.basename(link)
        current_time = time.strftime('%Y-%m-%d_%H:%M:%S')
        remote_folder = self.file_folder + current_time

        create_folder_command = f"mkdir -p {remote_folder}"
        subprocess.run(f"ssh root@{droplet_ip} '{create_folder_command}'", shell=True)

        file_path = os.path.join(remote_folder, file_name)

        with requests.get(link, stream=True) as r:
            r.raise_for_status()
            with subprocess.Popen(f"ssh root@{droplet_ip} 'cat > {file_path}'", shell=True, stdin=subprocess.PIPE) as p:
                for chunk in r.iter_content(chunk_size=8192):
                    p.stdin.write(chunk)
        uploaded_time = time.strftime('%Y-%m-%d_%H:%M:%S')
        end_time = time.time()
        time_spent = round(end_time - start_time, 3)
        upload_response = {
            "filename": file_name,
            "time_spent": time_spent,
            "host_ip": droplet_ip,
            "time_when_upload": uploaded_time,
            "file_path": f"{current_time}/{file_name}"
        }
        return upload_response

    def sync_uploaded_file(self, droplet_ip: str) -> list:

        sync_response = []
        for droplet in self.droplets:
            if droplet[0] != droplet_ip:
                start_time = time.time()
                ssh_command = f"ssh root@{droplet_ip} 'rsync -avz --delete {self.file_folder} root@{droplet[0]}:{self.file_folder}'"
                subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
                end_time = time.time()
                uploaded_time = time.strftime('%Y-%m-%d_%H:%M:%S')
                result = {
                    "vps": droplet[1],
                    "time_when_upload": uploaded_time,
                    "time_to_sync": round(end_time - start_time, 3),
                    "droplet_ip": droplet[0],
                }
                sync_response.append(result)

        return sync_response

    def get_file_download_command(self, file_path: str, droplet_ip: str) -> str:
        return f"ssh root@{droplet_ip} 'cat {self.file_folder}{file_path}'"
