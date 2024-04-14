import json
import configparser


def load_json(filename='google_c/client_secret_google.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def read_config():
    config = configparser.ConfigParser()
    config.read('system/config.ini')

    username = config['instagram_username']['username']
    password = config['instagram_password']['password']

    return username, password


def read_token():
    config = configparser.ConfigParser()
    config.read('system/config.ini')
    token = config['yandex_disk_token']['token']

    return token


def read_links():
    config = configparser.ConfigParser()
    config.read('system/config.ini')
    links = config['google_sheets_link']['links']

    return links
