from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from framework.healing.healing_engine import HealingEngine


class SmartElement:

    def __init__(
        self,
        driver,
        locator,
        expected_tag,
        expected_text,
        expected_type,
        expected_name,
        expected_class,
        reporter,
        name
    ):

        self.driver = driver
        self.locator = locator
        self.expected_tag = expected_tag
        self.expected_text = expected_text
        self.expected_type = expected_type
        self.expected_name = expected_name
        self.expected_class = expected_class
        self.reporter = reporter
        self.name = name

        self.healing_engine = HealingEngine(driver)

    def click(self):

        try:

            element = self.driver.find_element(
                *self.locator
            )

            element.click()

        except NoSuchElementException:

            result = self.healing_engine.heal(
                self.expected_text,
                self.expected_tag,
                self.expected_type,
                self.expected_name,
                self.expected_class
            )

            if not result:

                raise Exception(
                    f"Unable to heal element: {self.name}"
                )

            element = result["element"]
            confidence = result["confidence"]

            healed_locator = self.get_locator(
                element
            )

            self.reporter.add_event(
                self.name,
                self.locator,
                healed_locator,
                confidence
            )

            element.click()

    def get_locator(self, element):

        element_id = element.get_attribute("id")

        if element_id:

            return (
                By.ID,
                element_id
            )

        element_name = element.get_attribute("name")

        if element_name:

            return (
                By.NAME,
                element_name
            )

        return (
            By.TAG_NAME,
            element.tag_name
        )