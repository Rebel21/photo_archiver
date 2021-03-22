from vk_api_client import VkApiClient
from yandex_disk_api_client import YandexDiskApiClient

vk_user_id = input('Введите id пользователя VK: ')
if vk_user_id == '':
    vk_user_id = None
yandex_token = input('Введите токен Яндекс.Диск: ')
if yandex_token == '':
    yandex_token = None

vk_client = VkApiClient()
yandex_disk_client = YandexDiskApiClient(api_token=yandex_token)

user_id = vk_client.get_owner_id()
photos = vk_client.get_profile_photos(user_id=user_id)
path = yandex_disk_client.create_folder()
yandex_disk_client.upload_photos(photo_list=photos, path=path)