import json


def load_json(filename='google_c/client_secret_google.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def load_json_username(filename='system/instagram_username.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        username = json.load(f)
    return username


def load_json_password(filename='system/instagram_password.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        password = json.load(f)
    return password


def load_json_proxy_options(filename='system/proxy.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        proxy_options = json.load(f)
    return proxy_options


def load_json_token(filename='system/token.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        token = json.load(f)
    return token


def load_json_links(filename='system/links.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        links = json.load(f)
    return links
