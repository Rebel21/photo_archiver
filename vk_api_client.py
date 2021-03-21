import os
from pprint import pprint as pp

import requests


class VkApiClient:
    URL = 'https://api.vk.com/method/'

    def __init__(self, api_token=None, api_version='5.130'):
        if api_token is None:
            self.api_token = os.environ['VK_API_KEY']
        else:
            self.api_token = api_token
        self.api_version = api_version
        self.base_params = {
            'access_token': self.api_token,
            'v': self.api_version
        }

    def get_owner_id(self):
        owner_id_url = self.URL + 'users.get'
        owner_id = requests.get(owner_id_url, params=self.base_params).json()['response'][0]['id']
        return owner_id

    def get_profile_photos(self, user_id):
        photo_list = []
        profile_photos_url = self.URL + 'photos.get'
        request_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': 100
        }
        photo_items = requests.get(
            profile_photos_url, params={**self.base_params, **request_params}).json()['response']['items']
        for item in photo_items:
            photo_list.append({
                'photo': item['sizes'][-1]['url'],
                'likes_count': item['likes']['count']
            })
        return photo_list


if __name__ == '__main__':
    client = VkApiClient()
    user_id = client.get_owner_id()
    pp(client.get_profile_photos(user_id))
