from loguru import logger
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def parsing_number_likes(browser):
    try:
        likes_element = browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/"
                                                       "section/main/div/div[1]/div[3]/div/div[1]/section/div/div/"
                                                       "span/a/span/span")
        likes_count = likes_element.text
        logger.info(f'Количество лайков: {likes_count}')
    except NoSuchElementException:
        likes_count = ""

    return likes_count
