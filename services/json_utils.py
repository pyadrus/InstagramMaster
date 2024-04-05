import json


def load_json(filename='google_c/client_secret_google.json'):
    """
    Чтение json файла
    :args filename: - путь до файла
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    return data
