import os
import urllib.request
import socket
import requests


class LocationResolver:
    def __init__(self):
        self.ipapi_key = os.environ.get('IPAPI_ACCESS_KEY')
        self.droplets_dict = {
            "North America": ("VPS2 New York", os.environ.get('NEW_YORK_IP')),
            "South America": ("VPS2 New York", os.environ.get('NEW_YORK_IP')),
            "Asia": ("VPS3 Singapore", os.environ.get('SINGAPORE_IP')),
            "Australia": ("VPS3 Singapore", os.environ.get('SINGAPORE_IP')),
            "Europe": ("VPS1 Frankfurt", os.environ.get('FRANKFURT_IP')),
            "Africa": ("VPS1 Frankfurt", os.environ.get('FRANKFURT_IP')),
        }

    @staticmethod
    def _get_ip_from_link(link: str) -> str:
        file_host = urllib.parse.urlparse(link).hostname
        link_ip = socket.gethostbyname(file_host)
        return link_ip

    def _get_continent(self, ip_address) -> str:
        response = requests.get(f'http://api.ipapi.com/api/{ip_address}?access_key={self.ipapi_key}').json()
        continent = response.get("continent_name")
        return continent

    def get_droplet_location(self, *args) -> tuple:
        if isinstance(*args, str):
            ip = self._get_ip_from_link(*args)
            continent = self._get_continent(ip)
            droplet_location = self.droplets_dict.get(continent)
            return droplet_location
        else:
            user_ip = args[0].remote_addr
            if user_ip == "127.0.0.1":
                user_ip = "195.225.229.194"
            continent = self._get_continent(user_ip)
            droplet_location = self.droplets_dict.get(continent)
            return droplet_location
