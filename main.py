from loguru import logger
from rich import print

from disk.disk import upload_file
from google_c.google_insta import google_insta
from instagram_pars.authorization import authorization_instagram_mobile
from instagram_pars.parsing_instagram import parsing_posts_from_a_page, download_posts_from_the_page

logger.add("log/log.log")

"""
Парсинг Instagram

Данные:
1. Дата поста ✔️
2. Время поста ✔️
3. День недели поста ✔️
5. Формат поста
6. Ссылка на пост в Instagram ✔️
7. Количество лайков ✔️
8. Количество (просмотров)
9. Количество комментариев ✔️
10. Количество репостов

Данные в Google Sheets
1. Дата поста
2. Время поста
3. День недели поста
5. Формат поста
6. Ссылка на пост в Instagram
7. Количество лайков
8. Количество (просмотров)
9. Количество комментариев
10. Количество репостов
11. Ссылка на спаренные файлы в Яндекс Диске
"""








def program_settings():
    pass


def download_post_instagram():
    pass


def download_reels_instagram():
    pass


def main() -> None:
    """Основная функция"""
    print(
        '[red][1] - Парсинг постов со страницы\n'
        '[red][2] - Парсинг reels со страницы\n'
        '[red][3] - Скачать посты instagram со страницы\n'
        '[red][4] - Скачать reels instagram со страницы\n'
        '[red][5] - Запись в google\n'
        '[red][6] - Работа с Яндекс диском'
        '[red][7] - Настройки'
    )
    user_input = input("Выбери действие ")
    if user_input == "1":  # Парсинг постов со страницы
        parsing_posts_from_a_page()
    elif user_input == "2":  # Парсинг reels со страницы
        browser = initialize_driver()  # Инициализация браузера
        authorization_instagram_mobile(browser)  # Авторизация
        download_posts_from_the_page(browser)  # Скачать посты в папку "downloaded_content" с названием поста
    elif user_input == "3":  # Скачать посты instagram со страницы
        download_post_instagram()
    elif user_input == "4":  # Скачать reels instagram со страницы
        download_reels_instagram()
    elif user_input == "5":  # Запись в google
        google_insta()
    elif user_input == "6":  # Работа с Яндекс диском
        upload_file()
    elif user_input == "7":  # Настройки
        program_settings()





if __name__ == '__main__':
    main()
