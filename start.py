import requests, time
import pytesseract
from selenium import webdriver
from bs4 import BeautifulSoup
import base64, re, os

class browser_emulator():
    def __init__(self, url):
        self.url = url
        self.emulator()

    def imgurl2text(self):

        new_str = self.img_data[self.img_data.find("\"") + len("\""):self.img_data.rfind("\"")]
        head, data = new_str.split(',', 1)
        file_ext = head.split(';')[0].split('/')[1]
        plain_data = base64.b64decode(data)
        file_name = "image." + file_ext
        with open(file_name, 'wb') as f:
            f.write(plain_data)
        phone_number = pytesseract.image_to_string(file_name)
        phone_number = re.sub('[-" "]', '', phone_number)
        print(phone_number)
        os.remove(file_name)

    def emulator(self):

        driver = webdriver.Firefox()
        driver.get(self.url)
        button = driver.find_element_by_class_name("item-phone-button-sub-text")
        button.click()
        soup = BeautifulSoup(driver.page_source, "lxml")
        true_img = ""
        for img in soup.find_all('img'):
            if "data:image/png" in str(img):
                true_img = str(img)
        if true_img != "":
            self.img_data = true_img
            self.imgurl2text()
        else:
            print("Ничего не найдено 😥")

        

        #item-extended-phone


class avito_parser():
    def __init__(self):
        self.base_url = "https://www.avito.ru/moskva"
        self.main_method()
        
    def main_method(self):
        session = requests.session()
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0"})
        page_counter = 1

        while page_counter != 8:
            dynamic_url = "/lichnye_veschi?s_trg=10&p=" + str(page_counter)
            htmltext = session.get(self.base_url + dynamic_url).text
            soup = BeautifulSoup(htmltext, "lxml")
            idlinks_list = []

            

            idlinks_list = list(set(idlinks_list))

            print("**Получили данные со страницы " + str(dynamic_url) + "**")
            page_counter += 1
            time.sleep(3)

#avito_parser()

browser_emulator("https://www.avito.ru/moskva/odezhda_obuv_aksessuary/steganaya_kurtka_barbour_chelsea_1526067487")