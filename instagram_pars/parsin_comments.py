from loguru import logger
from selenium.webdriver.common.by import By


def download_comments(browser, url):
    """
    Получение информации о количестве комментариев
    :param browser: браузер
    :param url: адрес поста
    """
    browser.get(url)  # Перейти на страницу поста
    posts_com = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div[3]/div/div[3]/a/span/span'
    likes_counts = browser.find_element(By.XPATH, posts_com)
    likes_count = likes_counts.text
    logger.info(f'Количество комментариев: {likes_count}')
    return likes_count



