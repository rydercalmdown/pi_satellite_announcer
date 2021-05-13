import os
import requests


class SpaceTrackApi():
    """model for interacting with the space-track.org API"""

    def __init__(self):
        self.username = os.environ['SPACETRACK_USERNAME']
        self.password = os.environ['SPACETRACK_PASSWORD']
        self.session = requests.Session()
        self.protocol = 'https'
        self.host = 'www.space-track.org'
        self.login()

    def login(self):
        """Logs in to the session for the API"""
        post_data = {
            'identity': self.username,
            'password': self.password,
        }
        endpoint = '/ajaxauth/login'
        url = f"{self.protocol}://{self.host}{endpoint}"
        response = self.session.post(url, data=post_data)
        if not response.reason == 'OK':
            raise Exception('Unable to login to spacetrack.org API')

    def get_all_tles(self):
        """Returns the list of all TLEs from the API"""
        endpoint = '/basicspacedata/query/class/gp/format/3le/emptyresult/show'
        url = f"{self.protocol}://{self.host}{endpoint}"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.text
