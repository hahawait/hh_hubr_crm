import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from apps.base.service import BaseService
from apps.hubr.models import CompanyModel, CompanyContactMemberModel, VacancyModel, CompanyContactMembersModel


class HubrService(BaseService):
    def _auth(self, url: str = "https://account.habr.com/login/"):
        self.driver.driver.get(url)

        email_field = self.driver.driver.find_element(By.ID, 'email_field')
        email_field.send_keys(self.config.hubr_settings.HUBR_EMAIL)

        password_field = self.driver.driver.find_element(By.ID, 'password_field')
        password_field.send_keys(self.config.hubr_settings.HUBR_PASSWORD)

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

    def _get_company_contact_member(self, url: str) -> CompanyContactMemberModel:
        self.driver.driver.get(url)

        limit_element = self.driver.find_by_class_name('no-content__description')
        if limit_element and "суточный лимит" in limit_element.text:
            print(limit_element.text)
            return

        contact_member = CompanyContactMemberModel(contact_name=self.driver.find_by_class_name('page-title__title').text)
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

    def get_company_contact_members(self) -> CompanyContactMemberModel:
        contact_members = []
        company = CompanyContactMembersModel(company_name=self.driver.find_by_class_name('company_name').text)
        contacts = self.driver.driver.find_elements(By.CLASS_NAME, 'company_public_member')
        for contact in contacts:
            try:
                link = contact.get_attribute('href')
                contact_member = self._get_company_contact_member(link)
                if not contact_member:
                    return
                contact_members.append(contact_member)
            except StaleElementReferenceException:
                continue
        company.contact_members.append(contact_members)
        return contact_members

    def get_company_contacts(self) -> CompanyModel:
        company = CompanyModel(company_name=self.driver.find_by_class_name('company_name').text)
        company_contacts_element = self.driver.find_by_class_name('contacts')
        if company_contacts_element:
            company_contacts = company_contacts_element.find_elements(By.CLASS_NAME, 'contact')

            for contact in company_contacts:
                # Получаем тип контакта
                contact_type = self.driver.find_in_web_element_by_class_name(contact, 'type').text
                # Получаем значение контакта
                contact_value = self.driver.find_in_web_element_by_class_name(contact, 'value').text
                company.contacts[contact_type[:-1]] = contact_value

        return company

    def _get_vacancy_list_from_page(self) -> list[VacancyModel]:
        vacancy_list = []

        vacancy_elements = self.driver.driver.find_elements(By.CLASS_NAME, 'vacancy-card')
        
        for element in vacancy_elements:
            # Находим элемент с классом vacancy-card__company и получаем текст из него
            company_name = self.driver.find_in_web_element_by_class_name(element, 'vacancy-card__company-title')

            # Находим элемент с классом vacancy-card__title и получаем текст из него
            title = self.driver.find_in_web_element_by_class_name(element, 'vacancy-card__title-link')

            # Находим элемент с классом basic-date и получаем текст из него
            date = self.driver.find_in_web_element_by_class_name(element, 'basic-date')

            # Находим элемент с классом basic-salary и получаем текст из него
            salary = self.driver.find_in_web_element_by_class_name(element, 'basic-salary')
            vacancy_list.append(
                VacancyModel(
                    company_name=company_name.text if company_name else company_name,
                    vacancy_name=title.text if title else title,
                    salary=salary.text if salary else salary,
                    date=date.get_attribute('datetime') if date else date,
                )
            )

        return vacancy_list

    def get_vacancy_list(self, url: str) -> list[VacancyModel]:
        vacancy_list = []
        self.driver.driver.get(url)
        time.sleep(0.2)

        while True:
            try:
                time.sleep(1)
                vacancy_list.extend(self._get_vacancy_list_from_page())

                # Находим кнопку "Следующая страница" по ее классу
                next_button = self.driver.driver.find_element(By.CSS_SELECTOR, '.with-pagination__side-button a[rel="next"]')
                # Кликаем на кнопку "Следующая страница"
                next_button.click()

            except NoSuchElementException:
                break

        self.driver.driver.close()

        return vacancy_list