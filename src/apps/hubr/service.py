import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from apps.base.service import BaseService
from apps.hubr.models import CompanyModel, ContactMemberModel


class HubrService(BaseService):
    def _auth(self, url: str = "https://account.habr.com/login/"):
        self.driver.driver.get(url)

        email_field = self.driver.driver.find_element(By.ID, 'email_field')
        email_field.send_keys(self.config.hubr_settings.EMAIL)

        password_field = self.driver.driver.find_element(By.ID, 'password_field')
        password_field.send_keys(self.config.hubr_settings.PASSWORD)

        input("Ввели капчу...\n")

    def _get_companies_url_from_page(self) -> list[str]:
        companies = self.driver.driver.find_elements(By.CLASS_NAME, 'companies-item')
        companies_url = []

        for company in companies:
            company_url = self.driver.find_in_web_element_by_class_name(company, 'title').get_attribute('href')
            companies_url.append(company_url)

        return companies_url

    def get_companies_url(self, url: str) -> list[str]:
        companies_url = []
        self.driver.driver.get(url)
        time.sleep(1)
        page_number = 1
        while True:
            try:
                companies_url.extend(self._get_companies_url_from_page())
                # Находим элемент страницы
                page_element = self.driver.driver.find_element(By.XPATH, '//a[@class="page  next "]')
                # Переходим на следующую страницу
                page_element.click()
                # Увеличиваем номер страницы
                page_number += 1
            except NoSuchElementException:
                # Если элемент не найден, выходим из цикла
                break
        self.driver.driver.close()
        return companies_url

    def _get_company_contact_member(self, url: str) -> ContactMemberModel:
        self.driver.driver.get(url)

        contact_member = ContactMemberModel(contact_name=self.driver.find_by_class_name('page-title__title').text)
        contact_elements = self.driver.driver.find_elements(By.CLASS_NAME, 'user-page-sidebar__contact-item')

        for contact_element in contact_elements:
            contacts_info = contact_element.find_elements(By.TAG_NAME, 'span')
            contact_type = contacts_info[0].text
            try:
                contact_value = contacts_info[1].text
            except IndexError:
                contact_value = contact_element.find_element(By.TAG_NAME, 'a').text

            contact_member.contacts[contact_type[:-1]] = contact_value
        return contact_member

    def _get_company_contact_members(self) -> list[ContactMemberModel]:
        contact_members = []

        contacts = self.driver.driver.find_elements(By.CLASS_NAME, 'company_public_member')
        for contact in contacts:
            try:
                link = contact.get_attribute('href')
                contact_members.append(self._get_company_contact_member(link))
            except StaleElementReferenceException:
                continue

        return contact_members, len(contact_members)

    def _get_company_contacts(self, url: str) -> CompanyModel:
        self.driver.driver.get(url)

        company = CompanyModel(company_name=self.driver.find_by_class_name('company_name').text)
        total = 0
        company_contacts_element = self.driver.find_by_class_name('contacts')
        if company_contacts_element:
            company_contacts = company_contacts_element.find_elements(By.CLASS_NAME, 'contact')

            for contact in company_contacts:
                # Получаем тип контакта
                contact_type = self.driver.find_in_web_element_by_class_name(contact, 'type').text
                # Получаем значение контакта
                contact_value = self.driver.find_in_web_element_by_class_name(contact, 'value').text
                company.contacts[contact_type[:-1]] = contact_value

            company.contact_members, total = self._get_company_contact_members()

        return company, total

    def get_companies_contacts(self, urls: list[str]) -> list[CompanyModel]:
        companies = []

        self._auth()
        self.driver.driver.get(urls[0])
        input("Нажали войти...\n")

        limit = 0
        for url in urls:
            company, total = self._get_company_contacts(url)
            companies.append(company)
            limit += total
        print("TOTAL LIMIT: ", limit)
        return companies
