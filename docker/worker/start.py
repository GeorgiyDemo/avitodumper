# В переметрах yaml версия драйвера
import requests
import adparser_module
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import getsettings_module

class ParseLinksClass(object):
    def __init__(self):
        self.settings = getsettings_module.get_settings()
        self.base_url = "https://www.avito.ru"
        self.avito_parse()

    def avito_parse(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        page_counter = 1
        number_counter = 0

        while number_counter < self.settings["numbers_count"]:
            dynamic_url = self.settings["second_url"] + str(page_counter)
            driver.get(self.base_url + dynamic_url)
            soup = BeautifulSoup(driver.page_source, "lxml")
            for link in soup.findAll('a', attrs={'href': re.compile("^/"+self.settings["city_in_url"]+"/")}):
                if "js-item-slider item-slider" in str(link):
                    link_str = str(link)
                    new_link = link_str[link_str.find("<a class=\"js-item-slider item-slider\" href=\"") + len("<a class=\"js-item-slider item-slider\" href=\""):link_str.rfind("\"> <ul class=\"item-slider-list js-item-slider-list\">")]
                    obj = adparser_module.advertisement_parser(self.base_url + new_link, driver, self.settings)
                    if obj.result == True:
                        number_counter += 1
                        if number_counter == self.settings["numbers_count"]:
                            break
            page_counter += 1

ParseLinksClass()