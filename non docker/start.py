#Кол-во номеров
#Ссылка
#Подссылка
#Длинна номера для фильтрации

import requests, time
import writer_module
import pytesseract
from selenium import webdriver
from bs4 import BeautifulSoup
import base64, re, os
from PIL import Image

class browser_emulator():
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
        self.emulator()

    def emulator(self):
        print("Работаем с URL "+self.url)
        driver = self.driver
        driver.get(self.url)
        try:
            button = driver.find_element_by_class_name("item-phone-button-sub-text")
            button.click()
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "lxml")
        except:
            print("ЛОЛ, КНОПКИ С НОМЕРОМ ТЕЛЕФОНА НЕТ НА СТРАНИЦЕ")

#TODO TRY CATCH 
        #Поиск имени
        for data in soup.find_all('div',{'class':'seller-info-name js-seller-info-name'}):
            username = data.getText()
        username = re.sub('[" "\n]', '', username)
        print(username)

#TODO TRY CATCH 
        #Тип пользоватля (компания/частное лицо/арендодатель и т.д.)
        for data in soup.find_all('div',{'class':'seller-info-col'}):
            buf_usertype = data.getText()
        buf_usertype_list = buf_usertype.split("\n")
        buf_usertype_list = list(filter(None, buf_usertype_list))
        usertype = buf_usertype_list[len(buf_usertype_list)-2]
        print(usertype)

        #Определение текста на изображении
        true_img = ""
        self.number_result = False
        for img in soup.find_all("img"):
            if "data:image/png" in str(img):
                true_img = str(img)
        if true_img != "":
            self.img_data = true_img
            self.imgurl2text()
            if self.number_result != False:
                #TODO Запись данных куда там надо
                print(self.number_result)
                writer_module.writer_class(self.number_result)

        else:
            print("Ничего не найдено 😥")

    def imgurl2text(self):

        new_str = self.img_data[self.img_data.find("\"") + len("\""):self.img_data.rfind("\"")]
        head, data = new_str.split(',', 1)
        file_ext = head.split(';')[0].split('/')[1]
        plain_data = base64.b64decode(data)
        file_name = "image." + file_ext
        with open(file_name, 'wb') as f:
            f.write(plain_data)
        im = Image.open(file_name)
        im = im.convert("RGB")
        im.save("image.jpg")
        phone_number = pytesseract.image_to_string("image.jpg")
        phone_number = re.sub('[\-" "]', '', phone_number)
        if len(phone_number) == 11:
            self.number_result = phone_number
        else:
            print("Ойй, номер какой-то странный")
        os.remove(file_name)
        os.remove("image.jpg")

class parse_links_class():
    def __init__(self):
        self.base_url = "https://www.avito.ru"
        self.avito_parse()

    def avito_parse(self):
        page_counter = 1
        driver = webdriver.Chrome()

        while page_counter != 5:
            dynamic_url = "/moskva/lichnye_veschi?s_trg=10&p=" + str(page_counter)
            driver.get(self.base_url + dynamic_url)
            soup = BeautifulSoup(driver.page_source, "lxml")
            for link in soup.findAll('a', attrs={'href': re.compile("^/moskva/")}):
                if "js-item-slider item-slider" in str(link):
                    link_str = str(link)
                    new_link = link_str[link_str.find("<a class=\"js-item-slider item-slider\" href=\"") + len("<a class=\"js-item-slider item-slider\" href=\""):link_str.rfind("\"> <ul class=\"item-slider-list js-item-slider-list\">")]
                    browser_emulator(self.base_url + new_link, driver)

            page_counter += 1

parse_links_class()