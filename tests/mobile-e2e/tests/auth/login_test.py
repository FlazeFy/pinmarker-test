from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestLogin:
    def test_user_can_login_with_valid_data(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        # Validate current page title
        assert "Welcome Back" in login_page.get_page_title(), "Page title mismatch"
        
        # Execute login with credential
        login_page.do_login("tester_user", "admin")

        # Current page
        assert dashboard_page.is_on_dashboard(), "User should be navigated to dashboard after login"

    def test_user_cant_login_with_wrong_password(self, driver):
        login_page = LoginPage(driver)

        # Validate current page title
        assert "Welcome Back" in login_page.get_page_title(), "Page title mismatch"
        
        # Execute login with credential
        login_page.do_login("tester_user", "admin4")

        # Validate error message
        assert login_page.get_error_message() == "wrong username or password", "Error message mismatch"
        driver.tap([(200, 400)])

        # Validate current page title
        assert "Welcome Back" in login_page.get_page_title(), "Page title mismatch"        

    def test_user_cant_login_with_empty_field(self, driver):
        login_page = LoginPage(driver)

        # Validate current page title
        assert "Welcome Back" in login_page.get_page_title(), "Page title mismatch"
        
        # Execute login with credential
        login_page.do_login("tester_user", " ")

        # Validate error message
        assert login_page.get_error_message() == "username and password cannot be empty", "Error message mismatch"
        driver.tap([(200, 400)])

        # Validate current page title
        assert "Welcome Back" in login_page.get_page_title(), "Page title mismatch"

    def test_user_cant_login_with_invalid_char_length(self, driver):
        login_page = LoginPage(driver)

        # Validate current page title
        assert "Welcome Back" in login_page.get_page_title(), "Page title mismatch"
        
        # Execute login with credential
        login_page.do_login("tes", "12")

        # Validate error message
        list_message = ["validation failed", "The Username or Email field must be at least 5 characters in length", "The Password field must be at least 5 characters in length"]
        for dt in list_message:
            assert dt in login_page.get_error_message(), "Error message mismatch"

        driver.tap([(200, 400)])

        # Validate current page title
        assert "Welcome Back" in login_page.get_page_title(), "Page title mismatch"      