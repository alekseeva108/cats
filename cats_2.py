from settings import yd_token

import requests
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_cat_image(text):
    logging.info(f'Запрашиваю картинку с текстом: "{text}"')
    url = f'https://cataas.com/cat/says/{text}'
    response = requests.get(url)

    if response.status_code != 200:
        logging.error(f'Не удалось получить картинку. Код ответа: {response.status_code}')
        sys.exit(0)

    logging.info(f'Картинка успешно получена. Тип содержимого: {response.headers["Content-Type"]}')
    return response.content


def create_folder(folder, headers):
    logging.info('Создаю папку на Яндекс Диске...')
    response = requests.put(
        'https://cloud-api.yandex.net/v1/disk/resources',
        headers=headers,
        params={'path': folder}
    )

    if response.status_code == 201:
        logging.info('Папка успешно создана')
    elif response.status_code == 409:
        logging.info('Папка уже существует, продолжаю...')
    else:
        logging.error(f'Ошибка при создании папки. Код ответа: {response.status_code}')
        sys.exit(0)


def get_upload_url(folder, filename, headers):
    logging.info('Запрашиваю URL для загрузки...')
    response = requests.get(
        'https://cloud-api.yandex.net/v1/disk/resources/upload',
        headers=headers,
        params={
            'path': f'disk:/{folder}/{filename}',
            'overwrite': 'true'
        }
    )

    if response.status_code != 200:
        logging.error(f'Ошибка получения URL для загрузки: {response.text}')
        sys.exit(0)

    logging.info('URL для загрузки получен')
    return response.json()['href']


def upload_image(upload_url, image_data, folder, filename):
    logging.info(f'Загружаю картинку "{filename}" на Яндекс Диск...')
    response = requests.put(upload_url, data=image_data)

    if response.status_code == 201:
        logging.info(f'Картинка успешно загружена в папку {folder}/{filename}')
    else:
        logging.error(f'Ошибка загрузки. Код ответа: {response.status_code}')


def main():
    folder = 'QAMIDPY-132'
    headers = {'Authorization': f'OAuth {yd_token}'}

    text = input('Введите текст для картинки с котиком: ')
    filename = f'{text}.jpg'

    image_data = get_cat_image(text)
    create_folder(folder, headers)
    upload_url = get_upload_url(folder, filename, headers)
    upload_image(upload_url, image_data, folder, filename)


if __name__ == '__main__':
    main()