import time
import re

from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException, TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from apps.base.service import BaseService
from apps.hh.models import VacancyModel


class HHService(BaseService):
    def auth(self, url: str = "https://hh.ru"):
        self.driver.driver.get(url)

        # Нахождение элемента "Войти" по CSS-селектору
        login_button = self.driver.find_by_css_selector(".supernova-button[data-qa='login']")

        # Клик на элемент "Войти"
        login_button.click()

        try:
            # Нахождение кнопки "Войти с паролем" по атрибуту data-qa
            login_with_password_button = self.driver.find_by_css_selector("button[data-qa='expand-login-by-password']")

            # Клик на кнопку "Войти с паролем"
            login_with_password_button.click()

            # Нахождение поля "Электронная почта или телефон" по атрибуту data-qa и ввод данных
            username_input = self.driver.find_by_css_selector("input[data-qa='login-input-username']")
            username_input.send_keys(self.config.hh_settings.HH_LOGIN)

            # Нахождение поля "Пароль" по атрибуту data-qa и ввод данных
            password_input = self.driver.find_by_css_selector("input[data-qa='login-input-password']")
            password_input.send_keys(self.config.hh_settings.HH_PASSWORD)

            time.sleep(1.5)

            login_button = self.driver.find_by_css_selector("button[data-qa='account-login-submit']")
            login_button.click()

        except AttributeError:
            # Нахождение элемента по атрибуту 'data-qa'
            login_with_password = self.driver.find_by_css_selector("[data-qa='expand-login-by-password']")
            login_with_password.click()

            username_input = self.driver.find_by_css_selector("[data-qa='login-input-username']")
            username_input.send_keys(self.config.hh_settings.HH_LOGIN)

            password_input = self.driver.find_by_css_selector("[data-qa='login-input-password']")
            password_input.send_keys(self.config.hh_settings.HH_PASSWORD)

            time.sleep(1.5)

            login_button = self.driver.find_by_css_selector("[data-qa='account-login-submit']")
            login_button.click()

        time.sleep(1.5)

    def auth_with_captcha(self):
        self.auth()
        input("Ввели капчу и нажали войти. (Нажмите Enter)")

    def _get_contact_buttons(self):
        return self.driver.driver.find_elements(By.CSS_SELECTOR, 'button[data-qa="vacancy-serp__vacancy_contacts"]')

    def _get_contacts(self) -> tuple[str, list[str], str, str]:
        time.sleep(2)
        contact_block = self.driver.find_by_class_name("vacancy-contacts-call-tracking")
        if not contact_block:
            contact_block = self.driver.find_by_class_name(
                "magritte-drop-container___dbMt9_6-0-7"
            )
        text = list(contact_block.text.strip().split('\n'))
        # print("TEXT:\n", text, '\n')
        # Регулярное выражение для номера телефона
        phone_pattern = r"\+7 \d{3} \d{6}"
        # Регулярное выражение для электронной почты
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        phone = re.search(phone_pattern, contact_block.text)
        email = re.search(email_pattern, contact_block.text)

        fio = text[0]
        phone = phone.group(0) if phone else None
        email = email.group(0) if email else None

        try:
            close_button = WebDriverWait(self.driver.driver, 0.5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "vacancy-contacts-call-tracking__close")))
            close_button.click()
        except TimeoutException:
            try:
                close_button = WebDriverWait(self.driver.driver, 0.5).until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "button[data-qa='bloko-drop-down-close-button']")))
                close_button.click()
            except TimeoutException:
                webdriver.ActionChains(self.driver.driver).send_keys(Keys.ESCAPE).perform()
        # print("RES: ", fio, phone, email, '\n\n')
        return fio, phone, email

    def _get_vacancy_list_from_page(self, url: str) -> list[VacancyModel]:
        vacancy_list = []

        time.sleep(0.5)
        self.driver.driver.get(url)
        time.sleep(0.5)

        buttons = self._get_contact_buttons()

        for button in buttons:

            self.driver.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            vacancy = button.find_element(By.XPATH, "../../../../..")

            text = list(vacancy.text.strip().split('\n'))

            salary = None
            # Фильтрация текста
            if 'Сейчас' in text[0]:
                text = text[1:]
            vacancy_name = text[0]
            salary = text[1] if 'до вычета' or 'на руки' in text[1] else None
            company = text[3] if 'Можно удалённо' not in text[3] else text[4]

            try:
                vacancy_link = vacancy.find_element(By.CSS_SELECTOR, "a[data-qa='serp-item__title']")
            except NoSuchElementException:
                vacancy_link = vacancy.find_element(By.CSS_SELECTOR, "span.serp-item__title-link-wrapper a.bloko-link")

            # Кликаем на кнопку
            try:
                button.click()
            except Exception:
                continue

            fio, phone, email = self._get_contacts()

            vacancy_list.append(
                VacancyModel(
                    company_name=company,
                    vacancy_name=vacancy_name,
                    phone_numbers=phone,
                    email=email,
                    contact_name=fio,
                    salary=salary,
                    vacancy_link=vacancy_link.get_attribute("href") if vacancy_link else None
                )
            )

        return vacancy_list

    def get_vacancy(self, url: str, start_page: int, end_page: int) -> list[VacancyModel]:
        vacancy_list = []
        url += f"&page={start_page}"
        for i in range(start_page, end_page):
            vacancy_list.extend(self._get_vacancy_list_from_page(url))
            url = url.replace(f"&page={i}", f"&page={i+1}")
        self.driver.driver.close()
        return vacancy_list
