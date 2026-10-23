from selenium.webdriver.common.by import By

from framework.elements.smart_element import SmartElement


class LoginPage:

    def __init__(self, driver, reporter):

        self.driver = driver
        self.reporter = reporter

        self.login_button = SmartElement(
            driver,
            (By.ID, "loginButton"),
            "button",
            "Login",
            "submit",
            "signin",
            "login-button",
            reporter,
            "Login Button"
        )

    def click_login(self):

        self.login_button.click()