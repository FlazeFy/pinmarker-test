from appium import webdriver
from appium.options.android import UiAutomator2Options

class DriverManager:
    driver = None

    @classmethod
    def init_driver(cls):
        options = UiAutomator2Options()

        options.platform_name = "Android"
        options.platform_version = "14"
        options.device_name = "emulator-5554"
        options.automation_name = "UiAutomator2"
        options.app_package = "com.example.pinmarker"
        options.app_activity = "com.example.pinmarker.MainActivity"

        cls.driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        cls.driver.implicitly_wait(10)

        # print("Current Activity:", cls.driver.current_activity)
        # print("Page Source:")
        # print(cls.driver.page_source)

    @classmethod
    def get_driver(cls):
        return cls.driver

    @classmethod
    def quit_driver(cls):
        if cls.driver:
            cls.driver.quit()
            cls.driver = None