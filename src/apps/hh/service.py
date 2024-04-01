import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from settings import HHSettings
from apps.base.service import BaseService
from apps.base.models import VacancyModel


class HHService(BaseService):
    def hh_auth(self, url: str):
        self.driver.driver.get(url)

        # Нахождение элемента "Войти" по CSS-селектору
        login_button = self.driver.find_by_css_selector(
            ".supernova-button[data-qa='login']")

        # Клик на элемент "Войти"
        login_button.click()

        # Нахождение кнопки "Войти с паролем" по атрибуту data-qa
        login_with_password_button = self.driver.find_by_css_selector(
            "button[data-qa='expand-login-by-password']")

        # Клик на кнопку "Войти с паролем"
        login_with_password_button.click()

        # Нахождение поля "Электронная почта или телефон" по атрибуту data-qa и ввод данных
        username_input = self.driver.find_by_css_selector(
            "input[data-qa='login-input-username']")
        username_input.send_keys(self.config.hh_settings.LOGIN)

        # Нахождение поля "Пароль" по атрибуту data-qa и ввод данных
        password_input = self.driver.find_by_css_selector(
            "input[data-qa='login-input-password']")
        password_input.send_keys(self.config.hh_settings.PASSWORD)

        time.sleep(1.5)

        login_button = self.driver.find_by_css_selector(
            "button[data-qa='account-login-submit']")
        login_button.click()

        time.sleep(1.5)

    def _get_contact_buttons(self):
        return self.driver.driver.find_elements(By.CSS_SELECTOR, 'button[data-qa="vacancy-serp__vacancy_contacts"]')

    def get_vacancy(self, url: str):
        time.sleep(1)

        self.driver.driver.get(url)

        time.sleep(1)

        buttons = self._get_contact_buttons()

        count = 0
        for button in buttons:
            try:
                count += 1

                self.driver.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", button)
                vacancy = button.find_element(
                    By.XPATH, "ancestor::div[contains(@class, 'vacancy-serp-item__layout')]")
                vacancy_name = self.driver.find_in_web_element_by_css_selector(
                    vacancy, 'span.serp-item__title-link.serp-item__title[data-qa="serp-item__title"]')
                salary = self.driver.find_in_web_element_by_css_selector(
                    vacancy, 'span[data-qa="vacancy-serp__vacancy-compensation"].bloko-header-section-2')
                company = self.driver.find_in_web_element_by_css_selector(
                    vacancy, 'a[data-qa="vacancy-serp__vacancy-employer"].bloko-link_kind-tertiary')

                # Кликаем на кнопку
                button.click()

                # Ждем появления всплывающего окна
                WebDriverWait(self.driver.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "vacancy-contacts"))
                )

                time.sleep(0.02)

                # Находим блок div с контактными данными
                contact_block = self.driver.find_by_class_name(
                    "vacancy-contacts-call-tracking")
                if contact_block:
                    # Извлекаем ФИО
                    fio = self.driver.find_in_web_element_by_css_selector(
                        contact_block, "[data-qa='vacancy-contacts__fio'] span")
                    # Извлекаем телефоны
                    phones = []
                    phone_elements = contact_block.find_elements(
                        By.CLASS_NAME, "vacancy-contacts-call-tracking__phone-number")
                    for phone_element in phone_elements:
                        phone = phone_element.find_element(
                            By.TAG_NAME, "a").get_attribute("href")
                        phones.append(phone)
                    email = self.driver.find_in_web_element_by_css_selector(
                        contact_block, "[data-qa='vacancy-contacts__email']")
                    text = self.driver.find_in_web_element_by_css_selector(
                        contact_block, ".bloko-text_small span")
                else:
                    contact_block = self.driver.find_by_class_name(
                        "vacancy-contacts")
                    # Извлекаем ФИО
                    fio = self.driver.find_in_web_element_by_css_selector(
                        contact_block, "[data-qa='vacancy-serp__vacancy_contacts-fio']")
                    # Извлекаем телефоны
                    phones = []
                    phone_elements = contact_block.find_elements(
                        By.CLASS_NAME, "vacancy-contacts-call-tracking__phone-number")
                    for phone_element in phone_elements:
                        phone = phone_element.find_element(
                            By.TAG_NAME, "a").get_attribute("href")
                        phones.append(phone)
                    email = self.driver.find_in_web_element_by_css_selector(
                        contact_block, "[data-qa='vacancy-serp__vacancy_contacts-email']")
                    # Извлекаем текст
                    text = self.driver.find_in_web_element_by_css_selector(
                        contact_block, ".bloko-text_small span")

                print(vacancy_name.text if vacancy_name else vacancy_name)
                print(salary.text if salary else salary)
                print(company.text if company else company)

                print("ФИО:", fio.text if fio else fio)
                print("Телефоны:", phones)
                print("Email:", email.get_attribute("href").replace(
                    "mailto:", "") if email else email)
                print("Текст:", text.text if text else text)
                print("\n")

                # Находим кнопку
                close_button = WebDriverWait(self.driver.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@type='button' and @class='bloko-icon-link']"))
                )
                # Кликаем на кнопку
                close_button.click()

                time.sleep(0.02)

            except NoSuchElementException:
                continue
