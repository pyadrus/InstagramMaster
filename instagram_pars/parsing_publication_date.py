from datetime import datetime

from loguru import logger
from selenium.webdriver.common.by import By


def parsing_publication_date(browser):
    """
    Эта функция анализирует дату публикации поста и возвращает дату публикации в формате: 'YYYY-MM-DD'.
    :param browser: браузер
    :return: date_value - дата публикации,
             formatted_date - форматированная дата,
             formatted_time - форматированная время,
             day_of_week - день недели
    """
    posts_data = browser.find_element(By.CLASS_NAME,
                                      'x1p4m5qa')  # Получаем дату публикации поста (дата публикации)
    date_value = posts_data.get_attribute("datetime")  # Получаем значение атрибута datetime

    # Преобразуем строку в объект datetime
    datetime_object = datetime.strptime(date_value, "%Y-%m-%dT%H:%M:%S.%fZ")
    # Форматируем дату, время и день недели
    formatted_date = datetime_object.strftime("%Y-%m-%d")  # Дата публикации
    formatted_time = datetime_object.strftime("%H:%M:%S")  # Форматируем время
    day_of_week = datetime_object.strftime("%A").capitalize()  # Форматируем день недели
    # Выводим результаты
    logger.info(f"Дата поста: {formatted_date}")
    logger.info(f"Время поста: {formatted_time}")
    logger.info(f"День недели поста: {day_of_week}")

    return date_value, formatted_date, formatted_time, day_of_week
