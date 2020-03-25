'''
регион, возможность парсить подряд несколько регионов
настройка бд название таблицы формируется из дефолтного или указанного вручную
каталог баз данных(папка в которой лежат бд)
'''
from time import sleep
from config import main as config_main
from concurrent.futures.thread import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from webdriver import webdriver_conf
from config import InformationFromAds


def get_urls_from_page(url_page, ads_obj):
    html = requests.get(url_page).text
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all(attrs={"class": "snippet-link"})
    for page in pages:
        ads_obj.urls_ads.append(page.attrs['href'])
    if len(pages) == 0:
        driver = webdriver_conf.Webdriver().func_webdriver_window()
        driver.get(url_page)
        sleep(1)
        driver.get(url_page)
        sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        pages = soup.find_all(attrs={"class": "snippet-link"})
        for page in pages:
            ads_obj.urls_ads.append(page.attrs['href'])
        driver.close()


def get_info_from_page(ads_obj, regions, session, driver):
    # driver = webdriver_conf.Webdriver().func_webdriver()
    counter = 0

    #
    # print(driver)
    for url in ads_obj.urls_ads:
        url_page = "https://m.avito.ru" + url
        ads_obj.urls_ads.remove(url)
        driver.get(url_page)
        sleep(2)
        try:
            name2 = driver.find_elements_by_class_name('MXmyi')
            name = name2[-1].text
        except:
            name = 'None'
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
            button_link = driver.find_element_by_class_name('BPWk2')
            button_link.click()
            sleep(1)
            phone_number = driver.find_element_by_class_name('_3Ryy-').text[1:]
        except:
            phone_number = 'None'

        ads_ = {"phone": phone_number,
                        "name": name,
                        "title": title,
                        "price": price,
                        "place": place,
                        "description": description,
                        "type_ads": type_ads,
                        "region": regions,
                        "url": url}
        print(ads_)
        ads_obj.info_ads.append(ads_)
        counter += 1
        ad_db = InformationFromAds(**ads_)
        session.add(ad_db)
        if counter % 10 == 0:
            session.commit()
    session.commit()
    driver.close()


# все переменные для ввода хранятся в ..env
def main():
    av_request, regions, ads_obj, url_generator, session = config_main()
    urls = url_generator.urls(regions, av_request)
    cache_read = open('testbase', 'r')
    cache = [line.strip() for line in cache_read]
    cache_read.close()
    urls_obj = ads_obj.urls_ads
    webdriver = webdriver_conf.Webdriver()
    driver = webdriver.func_webdriver()
    if len(cache) == 0:
        with ThreadPoolExecutor(max_workers=2) as executor:
            for i in range(4, 100):
                url_page = urls + str(i)
                threads_ads = executor.submit(get_urls_from_page, url_page, ads_obj)
                cache_write = open('nedvij.txt', 'w')
                for i in ads_obj.urls_ads:
                    cache_write.write(i + '\n')
                cache_write.close()

        with ThreadPoolExecutor(max_workers=1) as executor:
            for i in range(0, 1):
                future = executor.submit(get_info_from_page, ads_obj, regions, session, driver)

    if len(cache) != 0:
        for i in cache:
            ads_obj.urls_ads.append(i)
        with ThreadPoolExecutor(max_workers=1) as executor:
            for i in range(0, 1):
                future = executor.submit(get_info_from_page, ads_obj, regions, session, driver)

    cache_write = open('cache.txt', 'w')
    for i in ads_obj.urls_ads:
        cache_write.write(i + '\n')
    cache_write.close()


    # for ad in ads_obj.info_ads:
    #     ad_db = InformationFromAds(**ad)
    #     session.add(ad_db)
    # session.commit()


if __name__ == '__main__':
    main()



