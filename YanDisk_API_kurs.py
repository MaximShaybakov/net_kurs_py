import os
import requests
import time
from progress.bar import IncrementalBar
from main import *



def run():
    ProfileYD = WriteYaDisk()
    ProfileYD.create_new_folder()
    ProfileYD.upload_file_to_disk()
    os.rmdir(f"{APIVk.get_headers()['owner_id']}")


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


    def create_new_folder(self):
        url = f'https://cloud-api.yandex.net/v1/disk/resources?path=%2FPhoto'
        response = requests.put(url, headers=self.headers)
        return response.json()


    def get_upload_link(self):
        '''
        Получение пути на яндекс.диск для загрузки Вашего файла.
        '''
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload?path=%2FPhoto/"
        headers = self.headers
        link_json_list = []
        with open(f'{APIVk.name()}/photo_info.json') as file:
            info = file.read()
        num_info = 0
        for name in self.write_photo():
            params = {"path": f'disk:/{name.strip()}', "overwrite": "true"}
            response = requests.get(upload_url + f'{name.strip()}', headers=headers, params=params, timeout=10)
            link_json_list.append(response.json())
            num_info += 1
        return link_json_list


    def write_photo(self):
        with open(f'{APIVk(self.ID)}/all_names.txt', 'r', encoding='utf-8') as file:
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
            response = requests.put(self.get_upload_link()[val_photo]['href'], data=open(f'photo/{name.strip()}', 'rb'))
            val_photo += 1
            time.sleep(1)
        bar.finish()
        if response.status_code == 201:
            print('Success!')
        else:
            print(f'Error {response.status_code}.')


if __name__ == '__main__':
    show_bar()
    run()