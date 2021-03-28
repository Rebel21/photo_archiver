import os
from datetime import datetime

import requests


def generate_photo_list(photo_list):
    """
    Функция добавляет к повторяющемуся имени фотографии, теущую дату
    """
    finish_photo_list = []
    for photo in photo_list:
        if len(finish_photo_list) > 0:
            if photo['file_name'] in [d['file_name'] for d in finish_photo_list]:
                photo['file_name'] = f'{photo["file_name"]}_{datetime.now().strftime("%d-%m-%Y")}.jpg'
                finish_photo_list.append(photo)
            else:
                finish_photo_list.append(photo)
        else:
            finish_photo_list.append(photo)
    return finish_photo_list


class VkApiClient:
    URL = 'https://api.vk.com/method/'

    def __init__(self, api_version='5.130'):
        self.api_token = os.environ['VK_API_KEY']
        self.api_version = api_version
        self.base_params = {
            'access_token': self.api_token,
            'v': self.api_version
        }

    def get_owner_id(self):
        """
        метод возвращает идентификатор текущего пользователя
        :return:
        """
        owner_id_url = self.URL + 'users.get'
        owner_id = requests.get(owner_id_url, params=self.base_params).json()['response'][0]['id']
        return owner_id

    def get_profile_photos(self, user_id):
        """
        Метод получает все фотографии профиля (ссылка на фото, размер, колличество лайков)
        :param user_id:
        :return:
        """
        photo_list = []
        profile_photos_url = self.URL + 'photos.get'
        request_params = {
            'owner_id': user_id if user_id is not None else self.get_owner_id(),
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': 100
        }
        photo_items = requests.get(
            profile_photos_url, params={**self.base_params, **request_params}).json()['response']['items']
        for item in photo_items:
            photo_list.append({
                'url': item['sizes'][-1]['url'],
                'file_name': f'{item["likes"]["count"]}.jpg',
                'size': item['sizes'][-1]['type']
            })
        return generate_photo_list(photo_list)
