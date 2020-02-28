import os
import requests
from bs4 import BeautifulSoup
from time import sleep
from concurrent.futures.thread import ThreadPoolExecutor
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
load_dotenv()
#
# class Webdriver():
#     def func_webdriver(): #todo переделать на класс, чтобы вызывая экземляр класса оставалась одна и та же сессия
#         path = os.getenv('chromedriver')
#         options = Options()
#         options.add_argument("--window-size=1500,1000")
#         options.add_argument("--disable-notifications")
#         # options.add_argument('--headless')
#         driver = webdriver.Chrome(executable_path=path, options=options)
#         return driver
#     driver = func_webdriver()

class Flats:
    def __init__(self):
        self.flats = []
        self.counter = 0
        self.urls = []

    def ret_flats(self):
        return self.flats

def get_urls_from_page(url_page, flats_obj):
    html = requests.get(url_page).text
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all(attrs={"class": "snippet-link"})
    # driver = webdriver.Chrome(r'C:\Users\Roman\PycharmProjects\avito parser v2\webdriver\chromedriver.exe')
    # driver.get(url_page)
    # driver.find_element_by_class_name('index-button-2q4Wv').click()
    # pages = driver.find_elements_by_class_name('snippet-link')
    for page in pages:
        flats_obj.urls.append(page.attrs['href'])


def get_info_from_page(url, flats_obj, region):
    chrome_options = webdriver.ChromeOptions()
    mobile_emulation = {"deviceName": "Nexus 5"}
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(
        executable_path=os.getenv('webdriver_path'),
        options=chrome_options)
    url_page = "https://m.avito.ru" + url
    driver.get(url_page)

    sleep(1)
    #todo проверить влияет ли всплывающее окно на доступ к другим элементам
    try:
        name2 = driver.find_elements_by_class_name('MXmyi')
        name = name2[-1].text
    except:
        name = 'None'
    button_link = driver.find_element_by_class_name('BPWk2')
    button_link.click()
    try:
        title = driver.find_element_by_class_name('_3Yuc4').text
    except:
        title = 'None'
    try:
        price = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[3]/div/div[1]/div/div[2]/p/span/span').text
    except:
        price = 'None'
    try:
        place = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[3]/div/div[3]/div/button/span').text
    except:
        place = 'None'
    try:
        description = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[4]/div[2]/div/div').text
    except:
        description = "None"
    try:
        type_ads = driver.find_element_by_class_name('naQ7K').text
    except:
        type_ads = "None"
    try:
        phone_number = driver.find_element_by_class_name('_3Ryy-').text
    except:
        phone_number = 'None'

    ads_ = {"phone": phone_number,
                    "name": name,
                    "title": title,
                    "price": price,
                    "place": place,
                    "description": description,
                    "type_ads": type_ads,
                    "region": region,
                    "url": url}
    driver.close()
    print(ads_)
    flats_obj.flats.append(ads_)


Base = declarative_base()


class InformationFromAds(Base):
    __tablename__ = os.getenv('tablename')
    id = Column(Integer, primary_key=True)
    phone = Column(String)
    name = Column(String)
    title = Column(String)
    price = Column(String)
    place = Column(String)
    description = Column(String)
    type_ads = Column(String)
    region = Column(String)
    url = Column(String)

    # def __repr__(self):
    #     return f'Квартира ID: {self.id}, имя: {self.title[:5]}'
    #
    # def __str__(self):
    #     return f'Квартира ID: {self.id}, имя: {self.title[:5]}'


engine = create_engine('sqlite:///' + os.getenv('database_name') + '.db')
session_object = sessionmaker()
session_object.configure(bind=engine)
Base.metadata.create_all(engine)
session = session_object()


def main():
    decode_zapros = os.getenv('zapros')
    zapros = decode_zapros.encode('cp1251').decode('utf8')
    region = os.getenv('region') # добавить потом, чтобы в БД сохранялся этот параметр как столбец.
    url = "https://www.avito.ru/" + str(region) + "/bytovaya_tehnika?p="
    flats_obj = Flats()
    with ThreadPoolExecutor(max_workers=1) as executor:
        for i in range(11, 20):
            url_page = url + str(i)
            threads_ads = executor.submit(get_urls_from_page, url_page, flats_obj)


    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in flats_obj.urls:
            future = executor.submit(get_info_from_page, url, flats_obj, region)

    counter = 0
    for flat in flats_obj.flats:
        counter +=1
        flat_db = InformationFromAds(**flat)
        session.add(flat_db)
        if counter % 10 == 0:
            session.commit()
    session.commit()


if __name__ == '__main__':
    main()

# veriables in .env file
# webdriver_path=C:\Users\Roman\PycharmProjects\avito parser v2\webdriver\chromedriver.exe
# zapros="ресницы"
# region=moskva
# database_name=llash
# tablename=lash large towns