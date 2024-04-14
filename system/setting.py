import configparser


class ConfigManager:
    def __init__(self, config_file='system/config.ini'):
        self.config_file = config_file

    def read_configs(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config

    def write_config(self, config):
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

    def update_config(self, section, key, value):
        config = self.read_configs()

        if not config.has_section(section):
            config.add_section(section)
        config.set(section, key, value)

        self.write_config(config)

    def update_instagram_credentials(self, username, password):
        self.update_config('instagram', 'username', username)
        self.update_config('instagram', 'password', password)

    def update_yandex_disk_token(self, token):
        self.update_config('yandex_disk', 'token', token)

    def update_google_sheets_link(self, link):
        self.update_config('google_sheets', 'link', link)


def program_settings():
    """Меню настроек программы"""
    config_manager = ConfigManager()
    print(
        '[1] Запись логина и пароля\n'
        '[2] Запись токена Яндекс Диск\n'
        '[3] Запись ссылки на Google Sheets\n'
    )

    user_input = input('Выберите вариант: ')
    if user_input == '1':
        username = input("Введите новый username: ")
        password = input("Введите новый password: ")
        config_manager.update_instagram_credentials(username=username, password=password)
    elif user_input == '2':
        token = input("Введите новый токен: ")
        config_manager.update_yandex_disk_token(token)
    elif user_input == '3':
        link = input("Введите ссылку на Google Sheets: ")
        config_manager.update_google_sheets_link(link)
    else:
        print('Вы ввели неверный номер')
        program_settings()


if __name__ == '__main__':
    program_settings()
