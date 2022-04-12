import os
import requests
from pprint import pprint
import time
from progress.bar import IncrementalBar


def run():
    ProfileYD = WriteYaDisk()
    ProfileYD.upload_file_to_disk()


class WriteYaDisk:

    def __init__(self): # инициализация класса для работы с api yandex disk
        self.token = self.get_token()
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }


    def get_token(self): # чтение токена для api yandex disk
        with open('tokens.txt') as file:  # укажите путь к файлу с вашим токеном к API VK
            token_ya = file.readlines()[1].strip()
        return token_ya


    def get_resp(self): # получение json всех данных на диске (печать на экран не обязательна)
        try:
            resp = requests.get(self.url, headers=self.headers, timeout=5)
            return resp.json()
        except KeyError:
            print('>>>>> [!] Invalid token Yandex. <<<<<')
            exit()


    def get_upload_link(self):
        '''
        Получение пути на яндекс.диск для загрузки Вашего файла.
        '''
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/"
        headers = self.headers
        link_json_list = []
        with open('photo/photo_info.json') as file:
            info = file.read()
        num_info = 0
        for name in self.write_photo():
            params = {"path": f'disk:/{name.strip()}', "overwrite": "true"}
            response = requests.get(upload_url + 'upload', headers=headers, params=params, timeout=10)
            link_json_list.append(response.json())
            num_info += 1
        return link_json_list


    def write_photo(self):
        with open('photo/all_names.txt', 'r', encoding='utf-8') as file:
            ls_name_photo = file.readlines()
        return ls_name_photo


    def upload_file_to_disk(self):
        '''
        Загрузка файла на яндекс диск.
        '''
        href = self.get_upload_link()
        headers = self.headers
        print('Copying files. Wait please...')
        val_photo = 0
        bar = IncrementalBar('Sending data to Yandex disk: ', max=len(self.write_photo()))
        for name in self.write_photo():
            bar.next()
            response = requests.put(href[val_photo].get("href", ""), data=open(f'photo/{name.strip()}', 'rb'))
            val_photo += 1
            time.sleep(1)
        bar.finish()
        if response.status_code == 201:
            print('Success!')
        else:
            print(f'Error {response.status_code}.')


if __name__ == '__main__':
    run()