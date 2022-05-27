import requests
import json
from tqdm import tqdm
from datetime import datetime
from YaDiskUpload import YaUploader


# # Для безопасности открывал токены таким образом на пк
# with open('vk_token.txt', 'r') as file_object:
#     token = file_object.read().strip()
#
# with open('ya_disk_token.txt', 'r') as file:
#     ya_token = file.read().strip()

token = input('Введите VK access_token: ')
ya_token = input('Введите токен с полигона Яндекс.Диска: ')
#


class VkUser:
    url = 'https://api.vk.com/method/'
    VkUser_id = input('Введите id пользователя: ')

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_user_avatar(self):
        user_url = self.url + 'photos.get'
        user_params = {
            'owner_id': self.VkUser_id,
            'album_id': 'profile',
            'photo_sizes': '1',
            'extended': '1'
        }
        req = requests.get(user_url, params={**self.params, **user_params}).json()
        return req['response']['items']

    def download_photo(self):
        ya_client = YaUploader(ya_token)
        photos = self.get_user_avatar()
        photo_names = []
        json_list = []
        # Добавлен прогресс-бар с помощью библиоткеи tqdm для наглядности отображения загрузки
        with tqdm(total=len(photos), desc='Downloading photos') as pbar:
            for photo in photos:
                sizes = photo['sizes']
                likes = photo['likes']['count']
                date_in_seconds = photo['date']
                normal_date = datetime.fromtimestamp(date_in_seconds).strftime('%Y-%m-%d %Hh%Mm')
                max_size_url = max(sizes, key=get_largest)['url']  # URL фото
                max_size_photo = max(sizes, key=get_largest)['type']  # Размер фото
                r = requests.get(max_size_url)
                filename = likes
                if filename not in photo_names:
                    ya_client.upload_file_to_disk(f'Netology/{filename}.jpg', r.content)
                    write_json(filename, max_size_photo, json_list)
                    photo_names.append(filename)
                else:
                    ya_client.upload_file_to_disk(f'Netology/{normal_date}.jpg', r.content)
                    write_json(normal_date, max_size_photo, json_list)
                pbar.update(1)
        with open('photos.json', 'a') as file:
            json.dump(json_list, file, indent=2, ensure_ascii=False)
        print('Successful download!')


def write_json(file_name, file_size, json_list):
    json_dict = dict()
    json_dict['file_name'] = str(file_name)
    json_dict['size'] = file_size
    json_list.append(json_dict)


def get_largest(size_dict):
    # Выясняю, горизонтально или вертикально-ориентирована фотография,
    # что бы далее мог отсортировать по нужному параметру словари

    if size_dict['width'] >= size_dict['height']:
        return size_dict['width']
    return size_dict['height']


if __name__ == '__main__':
    vk_client = VkUser(token, '5.131')
    vk_client.download_photo()
