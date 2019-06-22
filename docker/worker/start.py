#Кол-во номеров
#Ссылка
#Подссылка
#Длинна номера для фильтрации

import requests
import adparser_module
from selenium import webdriver
from bs4 import BeautifulSoup
import re

class parse_links_class():
    def __init__(self):
        self.base_url = "https://www.avito.ru"
        self.avito_parse()

    def avito_parse(self):
        page_counter = 4
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)

        while page_counter != 5:
            dynamic_url = "/moskva/lichnye_veschi?s_trg=10&p=" + str(page_counter)
            driver.get(self.base_url + dynamic_url)
            soup = BeautifulSoup(driver.page_source, "lxml")
            for link in soup.findAll('a', attrs={'href': re.compile("^/moskva/")}):
                if "js-item-slider item-slider" in str(link):
                    link_str = str(link)
                    new_link = link_str[link_str.find("<a class=\"js-item-slider item-slider\" href=\"") + len("<a class=\"js-item-slider item-slider\" href=\""):link_str.rfind("\"> <ul class=\"item-slider-list js-item-slider-list\">")]
                    adparser_module.advertisement_parser(self.base_url + new_link, driver)

            page_counter += 1

parse_links_class()