import pytest
from core.driver_manager import DriverManager

@pytest.fixture(scope="function")
def driver():
    DriverManager.init_driver()

    yield DriverManager.get_driver()

    DriverManager.quit_driver()