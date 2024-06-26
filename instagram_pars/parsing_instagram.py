import json
import math
import os
import random  # Импортируем модуль random, чтобы генерировать случайное число
import re
import time

import bs4
from bs4 import BeautifulSoup
from loguru import logger
from rich.progress import track
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from instagram_pars.authorization import authorization_instagram
from instagram_pars.download_video import download_from_instagram
from instagram_pars.parsin_comments import download_comments
from instagram_pars.parsing_number_likes import parsing_number_likes
from instagram_pars.parsing_post_descriptions import parsing_post_descriptions
from instagram_pars.parsing_publication_date import parsing_publication_date
from services.database import database_for_instagram_posts, removing_duplicates_from_the_database, get_instagram_posts
from services.working_with_files import download_image


def sanitize_folder_name(folder_name):
    """Преобразование названия папки"""
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']  # Заменяем недопустимые символы
    for char in invalid_chars:
        folder_name = folder_name.replace(char, '_')
    logger.info(f'Название папки {folder_name}')
    return folder_name


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
    # Change the user-agent of the webdriver
    # options = webdriver.ChromeOptions()
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    # Use the modified webdriver to log in to Instagram
    browser = webdriver.Chrome()  # Открываем браузер
    return browser


def parsing_posts_from_a_page(link, table) -> None:
    """
    Парсинг страницы с постами
    :arg link: ссылка на страницу профиля
    :arg table: таблица, в которую будут записываться посты
    """
    logger.info('Запуск скрипта')
    browser = initialize_driver()
    logger.info('Запуск браузера')
    authorization_instagram(browser)  # Авторизация
    logger.info(f'Переходим на страницу профиля {link}')
    browser.get(f"{link}")
    time.sleep(2)
    # Ищем элемент, содержащий количество публикаций
    posts = browser.find_element(By.CLASS_NAME, 'html-span')

    conn, cursor = database_for_instagram_posts(table)  # База данных для постов

    post_counter = posts.text  # # Считаем количество постов
    logger.info(f'Всего публикаций у пользователя: {post_counter}')
    number_of_posts = math.ceil(int(post_counter.replace(' ', '')) / 10)  # Считаем количество прокручиваний 382/10 = 38,2 (40 пролистываний)
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

    removing_duplicates_from_the_database(cursor, conn, table)  # Удаляем дубликаты из базы данных
    logger.info('Скролл страницы завершен')
    time.sleep(120)


def download_posts_from_the_page(browser, table) -> None:
    logger.info('Запуск скрипта по скачиванию постов')
    all_posts = get_instagram_posts(table)  # Запускаем скрипт для скачивания постов из базы данных.
    for post in all_posts:
        url = post[0]  # Extract the string from the tuple
        logger.info(f'Скачиваем пост: {url}')
        browser.get(url)  # Перейти на страницу поста
        display_progress_bar(time_1=4, time_2=5)  # Выводим прогресс бар для процесса режима ожидания
        amount_comments = download_comments(browser, url)  # Запускаем скрипт для скачивания комментариев
        date_value, formatted_date, formatted_time, day_of_week = parsing_publication_date(browser)
        likes_count = parsing_number_likes(browser)  # Получаем количество лайков
        description_text = parsing_post_descriptions(browser)  # Получаем описание поста
        folder_name = sanitize_folder_name(date_value)  # Преобразовываем в формат для имени папки
        folder_path = f'downloaded_content/{folder_name}/'  # Проверяем наличие папки
        os.makedirs(folder_path, exist_ok=True)
        try:
            video_src = ('/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/'
                         'div[1]/div/div/div/div/div/div/div/div/div/div/div/video')  # Видео пост
            browser.find_element(By.XPATH, video_src)
            logger.info('Видео')
            download_from_instagram(url, folder_path, f'{folder_name}.mp4')
        except NoSuchElementException:  # Если видео нет, то скачиваем картинку
            img_src = ("/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div[2]/"
                       "div/div/div/div/div/div[1]")  # Пост изображение
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
                    img_srcs = ('/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/'
                                'div[2]/div/div/div/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div/div[1]/img')
                    display_progress_bar(time_1=4, time_2=5)  # Выводим прогресс бар для процесса режима ожидания
                    posts = browser.find_element(By.XPATH, img_srcs).get_attribute('src')
                    download_image(posts, folder_path, f'{folder_name}_next{i - 1}.jpg')
        logger.info("Выключение браузера через 200 сек.")
        display_progress_bar(time_1=1, time_2=2)  # Выводим прогресс бар для процесса режима ожидания

        # Исправленный код:
        post_info = {
            "Дата поста": formatted_date,
            "Время поста": formatted_time,
            "День недели": day_of_week,
            "Количество лайков": likes_count,
            "Описание поста": description_text,
            "Количество комментариев": amount_comments,
            "Ссылка на пост": url,
        }

        logger.info(f'Информация о посте: {post_info}')
        writing_data_to_json_file(folder_path, folder_name, post_info)  # Записываем информацию в файл


if __name__ == '__main__':
    initialize_driver()  # Запускаем браузер
