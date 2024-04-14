import configparser


class ConfigManager:
    def __init__(self, config_file='system/config.ini') -> None:
        """Конструктор класса"""
        self.config_file = config_file

    def read_configs(self) -> configparser.ConfigParser:
        """Чтение конфигурации из файла"""
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config

    def write_config(self, config) -> None:
        """
        Запись конфига в файл config.ini
        :param config: конфиг в виде словаря
        """
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

    def update_config(self, section, key, value) -> None:
        """
        Обновление конфига
        :param section: раздел конфига в виде строки
        :param key: ключ в разделе конфига в виде строки
        :param value: значение в разделе конфига в виде строки
        """
        config = self.read_configs()

        if not config.has_section(section):
            config.add_section(section)
        config.set(section, key, value)

        self.write_config(config)

    def update_instagram_credentials(self, username, password) -> None:
        """
        Обновление данных для авторизации в инстаграме
        :param username: логин в инстаграме
        :param password: <PASSWORD>
        """
        self.update_config('instagram', 'username', username)
        self.update_config('instagram', 'password', password)

    def update_yandex_disk_token(self, token) -> None:
        """
        Обновление токена для доступа к Яндекс диску
        :param token: токен для доступа к Яндекс диску
        """
        self.update_config('yandex_disk', 'token', token)

    def update_google_sheets_link(self, link) -> None:
        """
        Обновление ссылки на гугл таблицу
        :param link: ссылка на гугл таблицу
        """
        self.update_config('google_sheets', 'link', link)

    def read_instagram_credentials(self) -> tuple[str, str]:
        """
        Чтение данных для авторизации в инстаграме
        :return: username, password
        """
        config = self.read_configs()
        username = config['instagram']['username']
        password = config['instagram']['password']
        return username, password

    def read_yandex_disk_token(self) -> str:
        """
        Чтение токена для доступа к Яндекс диску
        :return: токен для доступа к Яндекс диску
        """
        config = self.read_configs()
        token = config['yandex_disk']['token']
        return token

    def read_google_sheets_link(self) -> str:
        """
        Чтение ссылки на гугл таблицу
        :return: ссылка на гугл таблицу
        """
        config = self.read_configs()
        link = config['google_sheets']['link']
        return link


def program_settings() -> None:
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
