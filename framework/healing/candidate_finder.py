from selenium.webdriver.common.by import By


class CandidateFinder:

    def __init__(self, driver):

        self.driver = driver

    def find_candidates(self, expected_tag):

        candidates = self.driver.find_elements(
            By.TAG_NAME,
            expected_tag
        )

        return candidates