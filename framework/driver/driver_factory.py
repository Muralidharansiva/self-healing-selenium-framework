from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from framework.config.config_loader import ConfigLoader


class DriverFactory:

    @staticmethod
    def create_driver():

        config = ConfigLoader().get_browser_config()

        if config["name"].lower() != "chrome":

            raise Exception(
                f"Unsupported browser: {config['name']}"
            )

        options = Options()

        if config["headless"]:

            options.add_argument("--headless=new")

        options.add_argument(
            f"--window-size={config['window_width']},"
            f"{config['window_height']}"
        )

        driver = webdriver.Chrome(
            options=options
        )

        return driver