from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DriverFactory:

    @staticmethod
    def create_driver():

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)

        return driver