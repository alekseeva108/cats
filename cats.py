from settings import yd_token

import requests
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

text = input('Введите текст для картинки с котиком: ')
logging.info(f'Запрашиваю картинку с текстом: "{text}"')
url = f'https://cataas.com/cat/says/{text}'
response = requests.get(url)

if response.status_code != 200:
    print('Произошла какая-то ошибка')
    sys.exit(0)


print(response.headers['Content-Type'])
with open('cat.jpg', 'wb') as f:
    f.write(response.content)

image_data = response.content
filename = f'{text}.jpg'
logging.info('Создаю папку на Яндекс Диске...')
ya_headers = {'Authorization': f'OAuth {yd_token}'}
params = {'path': 'QAMIDPY-132'}
response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                        headers=ya_headers,
                        params=params)

logging.info('Запрашиваю URL для загрузки...')
upload_url_response = requests.get(
    'https://cloud-api.yandex.net/v1/disk/resources/upload',
    headers=ya_headers,
    params={
        'path': f'disk:/QAMIDPY-132/{filename}',  
        'overwrite': 'true'
    }
)
if upload_url_response.status_code != 200:
    print(f'Ошибка получения URL для загрузки: {upload_url_response.text}')
    sys.exit(0)

upload_url = upload_url_response.json()['href']

upload_response = requests.put(upload_url, data=image_data)

if upload_response.status_code == 201:
    print(f'Картинка успешно загружена на Яндекс Диск в папку QAMIDPY-132/{filename}')
else:
    print(f'Ошибка загрузки: {upload_response.status_code}')

