from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Controller:

    def __init__(self, path, url):
        self.driver = webdriver.Chrome(service=Service(path))
        self.url = url
        self.titles = list()
        self.authors = list()
        self.prices = list()

    def get_current_data(self):
        self.driver.get(self.url)
        elements = WebDriverWait(self.driver, 30).until(
            lambda x: x.find_elements(By.XPATH, "//*[@id='productList']"))
        self.titles.clear()
        self.authors.clear()
        self.prices.clear()
        index_field = 0
        for line in elements[0].text.splitlines():
            if index_field == 0:
                self.titles.append(line)
            elif index_field == 1:
                self.authors.append(line)
            elif index_field == 2:
                self.prices.append(line)
            index_field += 1
            if index_field > 2:
                index_field = 0
        self.driver.quit()

    def check_titles(self):
        self.get_current_data()
        return self.titles

    def check_authors(self):
        self.get_current_data()
        return self.authors

    def check_prices(self):
        self.get_current_data()
        return self.prices


