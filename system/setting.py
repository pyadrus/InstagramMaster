import configparser


def update_config(username, password):
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


def program_settings():
    """Меню настроек программы"""
    print('[1] Запись логина и пароля ')

    user_input = input('Выберите вариант: ')
    if user_input == '1':
        username = input("Введите новый username: ")
        password = input("Введите новый password: ")
        update_config(username, password)
    else:
        print('Вы ввели неверный номер')
        program_settings()


if __name__ == '__main__':
    program_settings()
