import json


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


def load_json_proxy(filename='system/proxy.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        proxy = json.load(f)
    return proxy


def load_json_proxy_options(filename='system/proxy.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        proxy_options = json.load(f)
    return proxy_options


def load_json_ClientID(filename='system/clientid.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        ClientID = json.load(f)
    return ClientID


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


def load_json_Client_secret(filename='system/Client_secret.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        Client_secret = json.load(f)
    return Client_secret


def load_json_passw(filename='system/passw.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        passw = json.load(f)
    return passw
