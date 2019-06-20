#Кол-во номеров
#Ссылка
#Подссылка
import requests, time
import pytesseract
from selenium import webdriver
from bs4 import BeautifulSoup
import base64, re, os
from PIL import Image

class advertisement_parser():
    """
    Класс для парсинга каждой отдельной страницы
    """
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
        self.emulator()

    def emulator(self):
        print("Работаем с URL "+self.url)
        driver = self.driver
        driver.get(self.url)
        button = driver.find_element_by_class_name("item-phone-button-sub-text")
        button.click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        
        #TODO необходимо получить тут следующую информацию:
        #номер - есть
        #Имя человека
        # Тип объявления (частное или компания)
        # URL страницы - есть
        true_img = ""
        for img in soup.find_all("img"):
            if "data:image/png" in str(img):
                true_img = str(img)
        if true_img != "":
            self.img_data = true_img
            self.imgurl2text()
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
        phone_number = re.sub('[-" "]', '', phone_number)
        print(phone_number)
        os.remove(file_name)
        os.remove("image.jpg")

class parse_links_class():
    """
    Класс для сбора ссылок с объявлениями
    """
    def __init__(self):
        self.base_url = "https://www.avito.ru"
        self.pages_parser()

    def pages_parser(self):
        page_counter = 7
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)

        while page_counter != 8:
            dynamic_url = "/moskva/lichnye_veschi?s_trg=10&p=" + str(page_counter)
            driver.get(self.base_url + dynamic_url)
            soup = BeautifulSoup(driver.page_source, "lxml")
            for link in soup.findAll('a', attrs={'href': re.compile("^/moskva/")}):
                if "js-item-slider item-slider" in str(link):
                    link_str = str(link)
                    new_link = link_str[link_str.find("<a class=\"js-item-slider item-slider\" href=\"") + len("<a class=\"js-item-slider item-slider\" href=\""):link_str.rfind("\"> <ul class=\"item-slider-list js-item-slider-list\">")]
                    advertisement_parser(self.base_url + new_link, driver)
            page_counter += 1

parse_links_class()
#driver = webdriver.Chrome()
#browser_emulator("https://www.avito.ru/moskva/odezhda_obuv_aksessuary/nike_1015483227", driver)