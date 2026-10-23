import pytest

from framework.driver.driver_factory import DriverFactory
from framework.reporting.healing_report import HealingReport


@pytest.fixture(scope="session")
def reporter():

    reporter = HealingReport()

    yield reporter

    reporter.save_report()


@pytest.fixture
def driver():

    driver = DriverFactory.create_driver()

    yield driver

    driver.quit()


@pytest.fixture(autouse=True)
def track_test(request, reporter):

    reporter.start_test(
        request.node.nodeid
    )