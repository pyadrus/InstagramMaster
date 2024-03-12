import json
import math
import os
import random  # Импортируем модуль random, чтобы генерировать случайное число
import re
import time

import bs4
from bs4 import BeautifulSoup
from loguru import logger
from rich import print
from rich.progress import track
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from instagram_pars.authorization import authorization_instagram, authorization_instagram_mobile
from instagram_pars.download_video import download_from_instagram
from instagram_pars.parsin_comments import download_comments
from services.database import database_for_instagram_posts, removing_duplicates_from_the_database, get_instagram_posts
from services.working_with_files import download_image
from system.config import proxy_options

logger.add("log/log.log")

"""
Парсинг Instagram

Данные:
1. Дата поста
2. Время поста
3. День недели поста
5. Формат поста
6. Ссылка на пост в Instagram
7. Количество лайков
8. Количество (просмотров)
9. Количество комментариев
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


def writing_data_to_json_file(folder_path, folder_name, post_info):
    """Функция, которая записывает данные в json файл"""
    with open(f'{folder_path}{folder_name}.json', 'w', encoding='utf-8') as file:
        # Создаем файл для записи данных
        json.dump(post_info, file, ensure_ascii=False)  # Сохраняем данные в файл


def display_progress_bar(time_1, time_2) -> None:
    """Отображаем время в виде progress bar"""
    # Генерируем случайное число в указанном диапазоне времени
    selected_shift_time = random.randrange(time_1, time_2)
    for _ in track(range(selected_shift_time),
                   description=f"[red]Спим {selected_shift_time} секунды/секунд..."):
        time.sleep(1)


def initialize_driver() -> webdriver:
    """Инициализация браузера"""
    browser = webdriver.Chrome(seleniumwire_options=proxy_options)  # Открываем браузер

    return browser


def parsing_posts_from_a_page() -> None:
    logger.info('Запуск скрипта')
    browser = initialize_driver()
    logger.info('Запуск браузера')
    authorization_instagram(browser)  # Авторизация
    logger.info('Переходим на страницу профиля https://www.instagram.com/anji_kn/')
    browser.get("https://www.instagram.com/anji_kn/")
    time.sleep(5)
    # Ищем элемент, содержащий количество публикаций
    posts = browser.find_element(By.CLASS_NAME, 'html-span')
    logger.info(f'Всего публикаций у пользователя: {posts.text}')
    conn, cursor = database_for_instagram_posts()  # База данных для постов
    number_of_posts = math.ceil(
        int(posts.text) / 10)  # Считаем количество прокручиваний 382/10 = 38,2 (40 пролистываний)
    logger.info(f'Количество пролистываний страницы {number_of_posts}')
    for _ in range(number_of_posts):
        # Скроллим страницу вниз
        browser.execute_script("window.scrollBy(0, 920);")  # 920 - количество пикселей для прокрутки
        # Ждем некоторое время (может потребоваться для загрузки контента)
        time.sleep(3)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')  # Инициализация BeautifulSoup
        # Находим все элементы с классом x1i10hfl, которые представляют собой ссылки на посты
        post_links = soup.find_all('a', class_='x1i10hfl')
        for post_link in post_links:  # Собираем все ссылки на посты
            # Используем два паттерна для поиска ссылок на посты и reels
            post_pattern = re.compile(r'/p/[\w\-]+/')
            reel_pattern = re.compile(r'/reel/[\w\-]+/')
            # Используем findall для поиска всех соответствующих ссылок
            post_links_found = post_pattern.findall(post_link['href'])
            reel_links_found = reel_pattern.findall(post_link['href'])
            for post_link_found in post_links_found:
                logger.info(f'Пост: {post_link_found}')
                post_url = f"https://www.instagram.com{post_link_found}"
                cursor.execute('INSERT INTO posts (post_url) VALUES (?)', (post_url,))
            for reel_link_found in reel_links_found:
                logger.info(f'Reel: {reel_link_found}')
                reel_url = f"https://www.instagram.com{reel_link_found}"
                cursor.execute('INSERT INTO posts (post_url) VALUES (?)', (reel_url,))
            conn.commit()

    removing_duplicates_from_the_database(cursor, conn)
    logger.info('Скролл страницы завершен')
    time.sleep(120)


def download_posts_from_the_page(browser) -> None:
    video_src = (
        '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div/div/div/video')  # Видео пост
    img_src = (
        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[1]/div/div/div/div/div/div/div[1]/div[1]")  # Пост изображение

    logger.info('Запуск скрипта по скачиванию постов')
    all_posts = get_instagram_posts()  # Запускаем скрипт для скачивания постов из базы данных.
    for post in all_posts:
        url = post[0]  # Extract the string from the tuple
        logger.info(f'Скачиваем пост: {url}')
        amount_comments = download_comments(browser, url)  # Запускаем скрипт для скачивания комментариев
        browser.get(url)  # Перейти на страницу поста
        display_progress_bar(time_1=1, time_2=3)  # Выводим прогресс бар для процесса режима ожидания
        posts_data = browser.find_element(By.CLASS_NAME,
                                          'x1p4m5qa')  # Получаем дату публикации поста (дата публикации)
        date_value = posts_data.get_attribute("datetime")  # Получаем значение атрибута datetime
        folder_name = sanitize_folder_name(date_value)  # Преобразовываем в формат для имени папки
        logger.info(f'Дата публикации поста: {date_value}')  # Выводим значение даты
        folder_path = f'downloaded_content/{folder_name}/'  # Проверяем наличие папки
        os.makedirs(folder_path, exist_ok=True)
        time.sleep(3)
        likes_element = browser.find_element(By.XPATH,
                                             "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/"
                                             "section/main/div/div[1]/div/div[2]/div/div[3]/section/div/div/"
                                             "span/a/span/span")
        likes_count = likes_element.text
        logger.info(f'Количество лайков: {likes_count}')
        time.sleep(3)
        try:
            # Получаем описание поста.
            description_element = browser.find_element(By.XPATH,
                                                       "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/"
                                                       "div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/"
                                                       "div/div[1]/div/div[2]/div/span/div/span")
            description_text = description_element.text
            logger.info(description_text)
            # Исправленный код:
            post_info = {"Дата публикации": date_value, "Количество лайков": likes_count,
                         "Описание поста": description_text, "Количество комментариев": amount_comments}

            logger.info(f'Информация о посте: {post_info}')
            writing_data_to_json_file(folder_path, folder_name, post_info)  # Записываем информацию в файл
            display_progress_bar(time_1=4, time_2=5)  # Выводим прогресс бар для процесса режима ожидания
            try:
                browser.find_element(By.XPATH, video_src)
                logger.info('Видео')
                download_from_instagram(url, folder_path, f'{folder_name}.mp4')
            except NoSuchElementException:  # Если видео нет, то скачиваем картинку
                browser.find_element(By.XPATH, img_src)
                logger.info('Изображение')
                html = browser.page_source  # Получаем html код страницы
                soup = bs4.BeautifulSoup(html, 'lxml')
                img_url = soup.select('._aagv  img')[0].get('src')
                logger.info(img_url)
                download_image(url=img_url, folder=folder_path, filename=f'{folder_name}.jpg')
                logger.info(f'Скачивание изображения: {img_url}')
                for i in range(1, 7):  # Download next two images
                    button_xpath = "//button[@aria-label='Далее']"
                    if browser.find_elements(By.XPATH, button_xpath):
                        browser.find_element(By.XPATH, button_xpath).click()
                        time.sleep(2)
                        posts = browser.find_element(By.XPATH, img_src).get_attribute('src')
                        time.sleep(3)
                        download_image(posts, folder_path, f'{folder_name}_next{i - 1}.jpg')
            logger.info("Выключение браузера через 200 сек.")
            display_progress_bar(time_1=1, time_2=2)  # Выводим прогресс бар для процесса режима ожидания
        except NoSuchElementException:
            description_text = ''
            # Исправленный код:
            post_info = {"Дата публикации": date_value, "Количество лайков": likes_count,
                         "Описание поста": description_text, "Количество комментариев": amount_comments}

            logger.info(f'Информация о посте: {post_info}')
            writing_data_to_json_file(folder_path, folder_name, post_info)  # Записываем информацию в файл
            display_progress_bar(time_1=4, time_2=5)  # Выводим прогресс бар для процесса режима ожидания
            try:
                browser.find_element(By.XPATH, video_src)
                logger.info('Видео')
                download_from_instagram(url, folder_path, f'{folder_name}.mp4')
            except NoSuchElementException:  # Если видео нет, то скачиваем картинку
                browser.find_element(By.XPATH, img_src)
                logger.info('Изображение')
                html = browser.page_source  # Получаем html код страницы
                soup = bs4.BeautifulSoup(html, 'lxml')
                img_url = soup.select('._aagv  img')[0].get('src')
                logger.info(img_url)
                download_image(url=img_url, folder=folder_path, filename=f'{folder_name}.jpg')
                logger.info(f'Скачивание изображения: {img_url}')
                for i in range(1, 7):  # Download next two images
                    button_xpath = "//button[@aria-label='Далее']"
                    if browser.find_elements(By.XPATH, button_xpath):
                        browser.find_element(By.XPATH, button_xpath).click()
                        display_progress_bar(time_1=4, time_2=5)  # Выводим прогресс бар для процесса ожидания
                        img_src = ('/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/'
                                   'div[1]/div/div[1]/div/div/div/div/div/div/div[1]/div[2]/div/div/div/ul/li[3]/'
                                   'div/div/div/div/div[1]/img')
                        posts = browser.find_element(By.XPATH, img_src).get_attribute('src')
                        logger.info(posts)
                        time.sleep(3)
                        download_image(posts, folder_path, f'{folder_name}_next{i - 1}.jpg')
            logger.info("Выключение браузера через 200 сек.")
            display_progress_bar(time_1=1, time_2=2)  # Выводим прогресс бар для процесса режима ожидания


def main() -> None:
    """Основная функция"""
    print('[red][1] - Парсинг постов со страницы\n'
          '[red][2] - Скачать посты со страницы\n'
          '[red][3]  - Скачать комментарии\n')
    user_input = input("Выбери действие ")
    if user_input == "1":
        parsing_posts_from_a_page()  # Парсинг постов со страницы сайта instagram
    elif user_input == "2":
        browser = initialize_driver()  # Инициализация браузера
        authorization_instagram_mobile(browser)  # Авторизация
        download_posts_from_the_page(browser)  # Скачать посты в папку "downloaded_content" с названием поста
    elif user_input == "3":
        browser = initialize_driver()  # Инициализация браузера
        authorization_instagram(browser)  # Авторизация
        download_comments(browser)


def sanitize_folder_name(folder_name):
    """Преобразование названия папки"""
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']  # Заменяем недопустимые символы
    for char in invalid_chars:
        folder_name = folder_name.replace(char, '_')
    logger.info(f'Название папки {folder_name}')
    return folder_name


if __name__ == '__main__':
    main()
