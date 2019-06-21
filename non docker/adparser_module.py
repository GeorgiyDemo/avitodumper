
import time
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
import writer_module
import pytesseract
import base64, re, os

class info_getter(object):
    """
    Класс с логикой парсинга данных из объекта bs
    """

    @staticmethod
    def get_username(soup_content):
        try:
            for data in soup_content.find_all('div',{'class':'seller-info-name js-seller-info-name'}):
                username = data.getText()
            username = re.sub('[" "\n]', '', username)
            return username
        except:
            return ""

    @staticmethod
    def get_usertype(soup_content):
        try:
            for data in soup_content.find_all('div',{'class':'seller-info-col'}):
                buf_usertype = data.getText()
            buf_usertype_list = buf_usertype.split("\n")
            buf_usertype_list = list(filter(None, buf_usertype_list))
            usertype = buf_usertype_list[len(buf_usertype_list)-2]
            return usertype
        except:
            return ""

    @staticmethod
    def get_usernumber(soup_content):
        true_img = ""
        for img in soup_content.find_all("img"):
            if "data:image/png" in str(img):
                true_img = str(img)
        if true_img != "":
            new_str = true_img[true_img.find("\"") + len("\""):true_img.rfind("\"")]
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
            os.remove(file_name)
            os.remove("image.jpg")
            if len(phone_number) == 11:
                return phone_number
            else:
                return ""
        return ""

class advertisement_parser():
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
            time.sleep(1) #<- Необходимо для прогрузки кода HTML после выполнения JS
            soup = BeautifulSoup(driver.page_source, "lxml")

            # Определяем имя пользователя
            username = info_getter.get_username(soup)
            #Тип пользоватля (компания/частное лицо/арендодатель и т.д.)
            usertype = info_getter.get_usertype(soup)
            #Номер пользователя
            usernumber = info_getter.get_usernumber(soup)
            print("Имя: "+username+"\nТип: "+usertype+"\nНомер: "+usernumber)

            #TODO - запись в БД (?)
            #writer_module.writer_class(number_result)
        except:
            print("ЛОЛ, КНОПКИ С НОМЕРОМ ТЕЛЕФОНА НЕТ НА СТРАНИЦЕ")
