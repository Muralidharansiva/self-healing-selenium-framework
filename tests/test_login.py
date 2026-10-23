import os

from selenium.webdriver.common.by import By

from framework.driver.driver_factory import DriverFactory
from framework.reporting.healing_report import HealingReport
from pages.login_page import LoginPage


class TestLogin:

    def setup_method(self):

        self.driver = DriverFactory.create_driver()
        self.reporter = HealingReport()

        file_path = os.path.abspath(
            "app/index.html"
        )

        self.driver.get(
            "file:///" + file_path
        )

    def teardown_method(self):

        self.driver.quit()

    def test_login_with_self_healing(self):

        login_page = LoginPage(
            self.driver,
            self.reporter
        )

        login_page.click_login()

        message = self.driver.find_element(
            By.ID,
            "message"
        )

        assert message.text == "Login successful"