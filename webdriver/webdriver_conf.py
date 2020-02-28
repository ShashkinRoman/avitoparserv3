import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from dotenv import load_dotenv
env_path = Path(r'C:\Users\Roman\PycharmProjects\avitoparserv3\.env')
load_dotenv(dotenv_path=env_path)




class Webdriver():
    def __init__(self, driver_=1):
        self.driver = driver_

    def func_webdriver(self):  # todo переделать на класс, чтобы вызывая экземляр класса оставалась одна и та же сессия
        options = Options()
        path = os.getenv('chrome_driver')
        mobile_emulation = {"deviceName": "Nexus 5"}
        options.add_argument("--disable-notifications")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=path, options=options)
        return self.driver

# def func_webdriver():  # todo переделать на класс, чтобы вызывая экземляр класса оставалась одна и та же сессия
#     options = Options()
#     path = os.getenv('chrome_driver')
#     mobile_emulation = {"deviceName": "Nexus 5"}
#     options.add_argument("--disable-notifications")
#     prefs = {"profile.managed_default_content_settings.images": 2}
#     options.add_experimental_option("prefs", prefs)
#     options.add_experimental_option("mobileEmulation", mobile_emulation)
#     # options.add_argument('--headless')
#     driver = webdriver.Chrome(executable_path=path, options=options)
#     return driver
#


