import configparser


def update_config(username, password) -> None:
    """
    Обновление username и password instagram в файле config.ini.
    :arg username: username instagram.
    :arg password: password instagram.
    """
    config = configparser.ConfigParser()
    config.read('system/config.ini')

    if not config.has_section('instagram_username'):
        config.add_section('instagram_username')
    config.set('instagram_username', 'username', username)

    if not config.has_section('instagram_password'):
        config.add_section('instagram_password')
    config.set('instagram_password', 'password', password)

    with open('system/config.ini', 'w') as configfile:
        config.write(configfile)


def update_config_disk(token) -> None:
    """
    Обновление token в файле config.ini.
    :arg token: token instagram.
    """
    config = configparser.ConfigParser()
    config.read('system/config.ini')
    if not config.has_section('yandex_disk_token'):
        config.add_section('yandex_disk_token')
    config.set('yandex_disk_token', 'token', token)

    with open('system/config.ini', 'w') as configfile:
        config.write(configfile)


def update_config_disk_link(link) -> None:
    """
    Обновление link в файле config.ini.
    :arg link: link instagram.
    """
    config = configparser.ConfigParser()
    config.read('system/config.ini')
    if not config.has_section('google_sheets_link'):
        config.add_section('google_sheets_link')
    config.set('google_sheets_link', 'link', link)


def program_settings():
    """Меню настроек программы"""
    print('[1] Запись логина и пароля\n'
          '[2] Запись токена Яндекс Диск\n'
          '[3] Запись ссылки на Google Sheets\n')

    user_input = input('Выберите вариант: ')
    if user_input == '1':
        username = input("Введите новый username: ")
        password = input("Введите новый password: ")
        update_config(username, password)
    elif user_input == '2':
        token = input("Введите новый токен: ")
        update_config_disk(token)
    elif user_input == '3':
        link = input("Введите ссылку на Google Sheets: ")
        update_config_disk_link(link)
    else:
        print('Вы ввели неверный номер')
        program_settings()


if __name__ == '__main__':
    program_settings()
