import os
import pytest
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage


class TestLogin:

    def test_login_with_self_healing(
        self,
        driver,
        reporter
    ):

        file_path = os.path.abspath(
            "app/index.html"
        )

        driver.get(
            "file:///" + file_path
        )

        login_page = LoginPage(
            driver,
            reporter
        )

        login_page.click_login()

        message = driver.find_element(
            By.ID,
            "message"
        )

        assert message.text == "Login successful"

    def test_login_with_name_change(
        self,
        driver,
        reporter
    ):

        file_path = os.path.abspath(
            "app/name_changed.html"
        )

        driver.get(
            "file:///" + file_path
        )

        login_page = LoginPage(
            driver,
            reporter
        )

        login_page.click_login()

        message = driver.find_element(
            By.ID,
            "message"
        )

        assert message.text == "Login successful"

    def test_login_fails_when_healing_is_ambiguous(
        self,
        driver,
        reporter
    ):

        file_path = os.path.abspath(
            "app/ambiguous.html"
        )

        driver.get(
            "file:///" + file_path
        )

        login_page = LoginPage(
            driver,
            reporter
        )

        with pytest.raises(
            Exception,
            match="multiple candidates"
        ):

            login_page.click_login()

    def test_login_fails_when_no_confident_candidate_exists(
        self,
        driver,
        reporter
    ):

        file_path = os.path.abspath(
            "app/no_good_candidate.html"
        )

        driver.get(
            "file:///" + file_path
        )

        login_page = LoginPage(
            driver,
            reporter
        )

        with pytest.raises(
            Exception,
            match="Unable to heal element: Login Button"
        ):

            login_page.click_login()