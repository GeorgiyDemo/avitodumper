import base64
import os
import re
import time

import pytesseract
import util_module
from PIL import Image
from bs4 import BeautifulSoup


class InfoGetter(object):
    """
    Класс с логикой парсинга данных из объекта bs
    """

    @staticmethod
    def get_username(soup_content):
        try:
            for data in soup_content.find_all(
                "div", {"class": "seller-info-name js-seller-info-name"}
            ):
                username = data.getText()
            username = re.sub('[" "\n]', "", username)
            return username
        except:
            return ""

    @staticmethod
    def get_usernumber(soup_content, number_length):
        true_img = ""
        for img in soup_content.find_all("img"):
            if "data:image/png" in str(img):
                true_img = str(img)
        if true_img != "":
            new_str = true_img[true_img.find('"') + len('"') : true_img.rfind('"')]
            head, data = new_str.split(",", 1)
            file_ext = head.split(";")[0].split("/")[1]
            plain_data = base64.b64decode(data)
            file_name = "image." + file_ext
            with open(file_name, "wb") as f:
                f.write(plain_data)
            im = Image.open(file_name)
            im = im.convert("RGB")
            im.save("image.jpg")
            phone_number = pytesseract.image_to_string("image.jpg")
            phone_number = re.sub('[\-" "]', "", phone_number)
            os.remove(file_name)
            os.remove("image.jpg")
            if len(phone_number) == number_length:
                return phone_number
        return ""

    @staticmethod
    def get_adtitle(soup_content):
        for data in soup_content.find_all("span", {"class": "title-info-title-text"}):
            return data.getText()


class advertisement_parser:
    def __init__(self, url, driver, sd):
        self.sd = sd
        self.result = False
        self.url = url
        self.driver = driver
        self.emulator()

    def emulator(self):
        driver = self.driver
        driver.get(self.url)
        # TODO ЧТО-ТО СДЕЛАТЬ
        time.sleep(2)
        try:
            button = driver.find_element_by_class_name("item-phone-button-sub-text")
            button.click()
            time.sleep(1)  # <- Необходимо для прогрузки кода HTML после выполнения JS
            soup = BeautifulSoup(driver.page_source, "lxml")

            # Определяем заголовок объявления
            adtitle = InfoGetter.get_adtitle(soup)
            # Определяем имя пользователя
            username = InfoGetter.get_username(soup)
            # Номер пользователя
            usernumber = InfoGetter.get_usernumber(soup, self.sd["phone_number_length"])
            if username != "" and usernumber != "":
                self.result = True
                print(
                    "\n*" + adtitle + "*\nИмя: " + username + "\nНомер: " + usernumber
                )
                util_module.TxtWorker("set", usernumber + "," + username + ";\n")
        except:
            pass
