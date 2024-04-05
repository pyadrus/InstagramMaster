import yadisk  # https://yadisk.readthedocs.io/ru/latest/
import requests

from system.config import load_json_token


def upload_file():
    endpoint = 'https://clck.ru/--'

    client = yadisk.Client(token=load_json_token())

    # Вы можете использовать либо конструкцию with, либо вручную вызвать client.close() в конце
    with client:
        print(client.check_token())  # Проверяет, валиден ли токен
        print(client.get_disk_info())  # Получает общую информацию о диске
        print(client.mkdir("Python_Disk"))  # Создаёт новую папку "/test-dir"
        yurl = client.get_download_link("Python_Disk")  # Возвращает ссылку на скачивание
        response = requests.get(endpoint, params={'url': yurl})
        t = response.text  # Возвращает ответ в виде ссылки
        print(t)


if __name__ == '__main__':
    upload_file()
