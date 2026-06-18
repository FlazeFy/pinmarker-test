from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class DashboardPage(BasePage):
    # Bottom Bar
    DASHBOARD_TAB = (AppiumBy.ACCESSIBILITY_ID, "Dashboard\nTab 1 of 4")

    def is_on_dashboard(self):
        try:
            element = self.driver.find_element(*self.DASHBOARD_TAB)
            # Check selected attribute
            return element.get_attribute("selected") == "true"
        except:
            return False