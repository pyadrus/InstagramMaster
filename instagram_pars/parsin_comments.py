from loguru import logger
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def download_comments(browser, url):
    """
    Получение информации о количестве комментариев
    :param browser: браузер
    :param url: адрес поста
    """
    try:
        likes_counts = browser.find_element(By.XPATH,
                                            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/'
                                            'div/div[1]/div[3]/div/div[3]/a/span/span')  # Количество комментариев
        likes_count = likes_counts.text
        logger.info(f'Количество комментариев: {likes_count} на странице {url}')
    except NoSuchElementException:
        likes_counts = browser.find_element(By.XPATH,
                                            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div[3]/div/div[2]/a/span/span')  # Количество комментариев
        likes_count = likes_counts.text
        logger.info(f'Количество комментариев: {likes_count} на странице {url}')

    return likes_count
