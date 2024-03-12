from loguru import logger
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def parsing_post_descriptions(browser):
    # Получаем описание поста.
    try:
        description_element = browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/"
                                                             "div[2]/section/main/div/div[1]/div[3]/div/div[2]/div/"
                                                             "span[2]/div/h1")
        description_text = description_element.text
        logger.info(f"Описание поста: {description_text}")
    except NoSuchElementException:
        description_text = ""

    return description_text
