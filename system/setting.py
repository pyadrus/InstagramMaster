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


def program_settings():
    """Меню настроек программы"""
    print('[1] Запись логина и пароля\n'
          '[2] Запить токена Яндекс Диск\n')

    user_input = input('Выберите вариант: ')
    if user_input == '1':
        username = input("Введите новый username: ")
        password = input("Введите новый password: ")
        update_config(username, password)
    elif user_input == '2':
        token = input("Введите новый токен: ")
        update_config_disk(token)
    else:
        print('Вы ввели неверный номер')
        program_settings()


if __name__ == '__main__':
    program_settings()
