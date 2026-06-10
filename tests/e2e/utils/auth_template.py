from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver, email, password):
    # Open login page
    driver.get("http://127.0.0.1:8080/LoginController")

    # Fill login form
    usernameInput = driver.find_element(By.ID, "username")
    usernameInput.clear()
    usernameInput.send_keys(email)

    passwordInput = driver.find_element(By.ID, "password")
    passwordInput.clear()
    passwordInput.send_keys(password)

    driver.find_element(
        By.CSS_SELECTOR,
        "#form-login .btn-submit"
    ).click()

    # Post condition
    WebDriverWait(driver, 10).until(
        lambda d: "/DashboardController" in d.current_url
    )