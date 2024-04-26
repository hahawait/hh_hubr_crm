import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from apps.base.service import BaseService
from apps.hh.models import VacancyModel


class HHService(BaseService):
    def _auth(self, url: str = "https://hh.ru"):
        self.driver.driver.get(url)

        # Нахождение элемента "Войти" по CSS-селектору
        login_button = self.driver.find_by_css_selector(".supernova-button[data-qa='login']")

        # Клик на элемент "Войти"
        login_button.click()

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

        time.sleep(1.5)

    def _get_contact_buttons(self):
        return self.driver.driver.find_elements(By.CSS_SELECTOR, 'button[data-qa="vacancy-serp__vacancy_contacts"]')

    def _get_contacts(self) -> tuple[str, list[str], str, str]:
        contact_block = self.driver.find_by_class_name("vacancy-contacts-call-tracking")
        if contact_block:
            # Извлекаем ФИО
            fio = self.driver.find_in_web_element_by_css_selector(contact_block, "[data-qa='vacancy-contacts__fio'] span")
            # Извлекаем телефоны
            phones = []
            phone_elements = contact_block.find_elements(By.CLASS_NAME, "vacancy-contacts-call-tracking__phone-number")
            for phone_element in phone_elements:
                phone = phone_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                phones.append(phone)
            email = self.driver.find_in_web_element_by_css_selector(contact_block, "[data-qa='vacancy-contacts__email']")
            text = self.driver.find_in_web_element_by_css_selector(contact_block, ".bloko-text_small span")
        else:
            contact_block = self.driver.find_by_class_name("vacancy-contacts")
            # Извлекаем ФИО
            fio = self.driver.find_in_web_element_by_css_selector(contact_block, "[data-qa='vacancy-serp__vacancy_contacts-fio']")
            # Извлекаем телефоны
            phones = []
            phone_elements = contact_block.find_elements(By.CLASS_NAME, "vacancy-contacts-call-tracking__phone-number")
            for phone_element in phone_elements:
                phone = phone_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                phones.append(phone)
            email = self.driver.find_in_web_element_by_css_selector(contact_block, "[data-qa='vacancy-serp__vacancy_contacts-email']")
            # Извлекаем текст
            text = self.driver.find_in_web_element_by_css_selector(contact_block, ".bloko-text_small span")
        email = email.get_attribute("href").replace("mailto:", "") if email else email

        return fio, phones, email, text

    def _get_vacancy_list_from_page(self, url: str) -> list[VacancyModel]:
        vacancy_list = []

        time.sleep(1)

        self.driver.driver.get(url)

        time.sleep(1)

        buttons = self._get_contact_buttons()

        for button in buttons:
            self.driver.driver.execute_script("arguments[0].scrollIntoView(true);", button)

            try:
                vacancy = button.find_element(By.XPATH, "ancestor::div[contains(@class, 'vacancy-serp-item__layout')]")
                vacancy_name = self.driver.find_in_web_element_by_css_selector(vacancy, 'span.serp-item__title-link.serp-item__title[data-qa="serp-item__title"]')
                salary = self.driver.find_in_web_element_by_css_selector(vacancy, 'span[data-qa="vacancy-serp__vacancy-compensation"].bloko-header-section-2')
                company = self.driver.find_in_web_element_by_css_selector(vacancy, 'a[data-qa="vacancy-serp__vacancy-employer"].bloko-link_kind-tertiary')
            except NoSuchElementException:
                # FIXME: REVIEW
                # vacancy = button.find_element(By.XPATH, "./ancestor::div[@class='serp-item']")
                vacancy = button.find_element(By.XPATH, "..")
                vacancy_name = vacancy.find_element(By.XPATH, ".//span[@class='vacancy-name--SYbxrgpHgHedVTkgI_cA serp-item__title-link serp-item__title-link_redesign']")
                company = vacancy.find_element(By.XPATH, ".//span[@class='company-info-text--O32pGCRW0YDmp3BHuNOP']")
                try:
                    salary = vacancy.find_element_by_xpath(".//span[@class='compensation-text--cCPBXayRjn5GuLFWhGTJ fake-magritte-primary-text--qmdoVdtVX3UWtBb3Q7Qj separate-line-on-xs--pwAEUI79GJbGDu97czVC']").text
                except NoSuchElementException:
                    salary = None

            vacancy_link =  self.driver.find_in_web_element_by_css_selector(vacancy, 'a.bloko-link')

            # Кликаем на кнопку
            try:
                button.click()
            except Exception:
                continue
            WebDriverWait(self.driver.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "vacancy-contacts")))
            time.sleep(0.2)

            fio, phones, email, text = self._get_contacts()

            vacancy_list.append(
                VacancyModel(
                    company_name=company.text if company.text else company,
                    vacancy_name=vacancy_name.text if vacancy_name else vacancy_name,
                    phone_numbers=phones,
                    email=email,
                    contact_name=fio.text if fio else fio,
                    salary=salary.text if salary else salary,
                    description=text.text if text else text,
                    vacancy_link=vacancy_link.get_attribute("href") if vacancy_link else None
                )
            )
            # Находим кнопку
            close_button = WebDriverWait(self.driver.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @class='bloko-icon-link']")))
            try:
            # Кликаем на кнопку
                close_button.click()
            except Exception:
                continue
            finally:
                time.sleep(0.2)

        return vacancy_list

    def get_vacancy(self, url: str, start_page: int, end_page: int) -> list[VacancyModel]:
        self._auth()
        vacancy_list = []
        url += f"&page={start_page}"
        for i in range(start_page, end_page):
            vacancy_list.extend(self._get_vacancy_list_from_page(url))
            url = url.replace(f"&page={i}", f"&page={i+1}")
        self.driver.driver.close()
        return vacancy_list
