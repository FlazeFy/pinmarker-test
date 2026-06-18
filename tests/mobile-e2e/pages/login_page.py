import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Title
    PAGE_TITLE = (AppiumBy.XPATH, "//*[@resource-id='page_title']")
    ERROR_MESSAGE = (AppiumBy.XPATH, "//*[@resource-id='error_alert']")

    # Input
    USERNAME_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
    PASSWORD_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')

    # Button
    LOGIN_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Sign In")')

    # Element handler
    def get_page_title(self):
        return self.driver.find_element(*self.PAGE_TITLE).get_attribute("content-desc")

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).get_attribute("content-desc")

    def enter_username(self, username):
        element = self.driver.find_element(*self.USERNAME_FIELD)
        element.click()
        element.clear()
        element.send_keys(username)

    def enter_password(self, password):
        element = self.driver.find_element(*self.PASSWORD_FIELD)
        element.click()
        element.clear()
        element.send_keys(password)

        print(element.text)
        print(element.get_attribute("text"))

    def click_login_button(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def do_login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

        time.sleep(5)