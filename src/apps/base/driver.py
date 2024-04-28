from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from settings import DriverSettings


class Driver:
    def __init__(self, driver_settings: DriverSettings) -> WebDriver:
        self.driver_settings = driver_settings
        options = Options()

        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Отключение показа всплывающих окон и уведомлений
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")

        # Отключить логи
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # Отключить ожидание полной загрузки страницы
        options.page_load_strategy = 'eager'

        # Фоновый режим
        # options.add_argument('--headless')

        # Создание драйвера Chrome с указанием пути к исполняемому файлу и объекта Options
        driver = webdriver.Chrome(
            service=Service(self.driver_settings.DRIVER_PATH), options=options)

        driver.maximize_window()

        self.driver = driver

    def restart(self):
        if self.driver:
            self.driver.quit()
            options = Options()

            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
            options.add_argument("--disable-blink-features=AutomationControlled")

            # Отключение показа всплывающих окон и уведомлений
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-notifications")

            # Отключить логи
            options.add_experimental_option("excludeSwitches", ["enable-logging"])

            # Отключить ожидание полной загрузки страницы
            options.page_load_strategy = 'eager'

            # Фоновый режим
            # options.add_argument('--headless')

            # Создание драйвера Chrome с указанием пути к исполняемому файлу и объекта Options
            driver = webdriver.Chrome(
                service=Service(self.driver_settings.DRIVER_PATH), options=options)

            driver.maximize_window()

            self.driver = driver

    def find_in_web_element_by_class_name(self, element: WebElement, value: str) -> str:
        try:
            return element.find_element(By.CLASS_NAME, value)
        except NoSuchElementException:
            return None

    def find_in_web_element_by_css_selector(self, element: WebElement, value: str) -> str:
        try:
            return element.find_element(By.CSS_SELECTOR, value)
        except NoSuchElementException:
            return None

    def find_by_class_name(self, value: str) -> str:
        try:
            return self.driver.find_element(By.CLASS_NAME, value)
        except NoSuchElementException:
            return None

    def find_by_css_selector(self, value: str) -> str:
        try:
            return self.driver.find_element(By.CSS_SELECTOR, value)
        except NoSuchElementException:
            return None
