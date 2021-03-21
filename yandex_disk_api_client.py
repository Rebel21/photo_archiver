import os
from datetime import datetime

import requests


class YandexDiskApiClient:
    URL = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, api_token=None):
        if api_token is None:
            self.api_token = os.environ['YANDEX_API_KEY']
        else:
            self.api_token = api_token

    def create_folder(self):
        current_date = datetime.now().strftime('%d-%m-%Y')
        create_folder_url = self.URL + 'resources'
        headers = {
            'Authorization': 'OAuth ' + self.api_token
        }
        params = {
            'path': f'disk:/archive_photos_from_vk_{current_date}'
        }
        response = requests.put(create_folder_url, headers=headers, params=params)
        return response


if __name__ == '__main__':
    client = YandexDiskApiClient()
    print(client.create_folder())
