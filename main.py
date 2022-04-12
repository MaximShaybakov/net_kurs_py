import json
import requests
from pprint import pprint
import time
from progress.bar import IncrementalBar
from YanDisk_API_kurs import run


def show_bar(): # функция запускает всю логику программы
    Profile_1 = APIVk()
    Profile_1.download_photo()


class APIVk: # инициализация класса
    def __init__(self):
        self.token = self.get_token()
        self.ID = int(input('Enter target ID: '))


    def get_token(self): # чтение токена из фа706йла
        with open('tokens.txt', 'rb') as file:  # укажите путь к файлу с вашим токеном к API VK
            token_vk = file.readlines()[0].strip()
        return token_vk


    def get_headers(self): # параметры запроса к api vk метода photos.get для ID 552934290
        return {
            'access_token': self.token, #токен обновлять ежедневно с разрешением на фото
            'owner_id': f'{self.ID}',
            'album_id': 'profile',
            'rev': '0',
            'extended': '1',
            'photo_size': '1',
            'v': '5.81'
        }


    def req_vk(self): #получение json файла фотографий профиля с API VK
        url = f'https://api.vk.com/method/photos.get'
        params = self.get_headers()
        response = requests.get(url, params=params, timeout=5)
        return response.json()


    def url_photo_max_size(self): # список url фото максимального размера
        ls_photo_max_size = []
        try:
            for url_photo in self.req_vk()['response']['items']:
                ls_photo_max_size.append(url_photo['sizes'][-1]['url'])
            return ls_photo_max_size
        except KeyError:
            print('>>>>> [!] Invalid token VK <<<<<')
            exit()


    def get_info_json(self): # создание файла json с данными о фото
        ls_json_info = []
        ls_name = []
        for val in self.req_vk()['response']['items']:
            if val['likes']['count'] not in ls_name:
                result = {
                    'name': f"{val['likes']['count']}",
                    'size': f"{val['sizes'][-1]['type']}",
                    'url': f"{val['sizes'][-1]['url']}"
                }
            else:
                result = {
                    'name': f"{val['date']}",
                    'size': f"{val['sizes'][-1]['type']}",
                    'url': f"{val['sizes'][-1]['url']}"
                }
            ls_name.append(val['likes']['count'])
            ls_json_info.append(result)
        with open('photo/photo_info.json', 'w', encoding='utf-8') as file: # запись данных в файл
            json.dump(ls_json_info, file, ensure_ascii=False, indent=4)
        return ls_json_info


    def ls_name(self): # создание списка с именами файлов и их запись в файл
        ls_name_photo = []
        with open('photo/all_names.txt', 'w') as file:
            for name_photo in self.get_info_json():
                ls_name_photo.append(name_photo['name'])
                file.write(name_photo['name'] + '.jpeg\n')
        with open('photo/all_names.txt', 'a') as f:
            f.write('photo_info.json')
        return ls_name_photo


    def download_photo(self): #загрузка фото с сервера на локальный диск в папку
        counter = 0
        bar = IncrementalBar('Receiving data from VK: ', max=len(self.url_photo_max_size()))
        for photo in self.url_photo_max_size():
            bar.next()
            img = requests.get(photo)
            with open(f"photo/{self.ls_name()[counter]}.jpeg", "wb") as file:
                file.write(img.content)
                counter += 1
                time.sleep(1)
        bar.finish()
        return


if __name__ == '__main__':
    show_bar()
    run()
