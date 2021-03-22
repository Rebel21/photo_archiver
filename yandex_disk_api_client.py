import os
from datetime import datetime

import requests


class YandexDiskApiClient:
    URL = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, api_token):
        if api_token is None:
            self.api_token = os.environ['YANDEX_API_KEY']
        else:
            self.api_token = api_token
        self.headers = {
            'Authorization': 'OAuth ' + self.api_token
        }

    def create_folder(self):
        current_date = datetime.now().strftime('%d-%m-%Y')
        create_folder_url = self.URL + 'resources'
        params = {
            'path': f'disk:/archive_photos_from_vk_{current_date}'
        }
        response = requests.put(create_folder_url, headers=self.headers, params=params)
        if response.status_code == 201:
            return params['path']
        else:
            return response.text

    def upload_photos(self, photo_list, path):
        upload_photo_url = self.URL + 'resources/upload'
        for photo in photo_list:
            file_name = f'{photo["likes_count"]}.jpg'
            params = {
                'path': f'{path}/{file_name}',
                'url': photo['photo']
            }
            response = requests.post(upload_photo_url, headers=self.headers, params=params)
            if response.status_code == 202:
                print({'file_name': file_name, 'size': photo['size']})
            else:
                return response.text
        return f'Загружено файлов: {len(photo_list)}'


if __name__ == '__main__':
    client = YandexDiskApiClient()
    print(client.create_folder())
