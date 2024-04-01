import time
from src.settings import get_config
# from src.apps.driver import get_driver
from src.apps.parser.hh.service import HHService

if __name__ == '__main__':
    url = "https://hh.ru/"
    config = get_config()
    # driver = get_driver(config.driver_settings.DRIVER_PATH)

    hh_service = HHService(
        config.driver_settings.DRIVER_PATH, config.hh_setting)
    hh_service.hh_auth(url)
    new_url = "https://hh.ru/search/vacancy?L_save_area=true&text=&excluded_text=&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50&hhtmFrom=vacancy_search_filter"
    hh_service.get_data(new_url)
    time.sleep(10000)
