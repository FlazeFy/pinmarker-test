from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given("I open the login page")
def step_open_login(context):
    context.driver = webdriver.Chrome()
    context.driver.get("http://127.0.0.1:8080/LoginController")

@then('I should see the section title "{title}"')
def step_title(context, title):
    el = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//h2[contains(text(), '{title}')]"))
    )
    assert el.is_displayed()

@then('I should see the label "{label}"')
def step_label(context, label):
    labels = context.driver.find_elements(By.CSS_SELECTOR, "#form-login label")
    texts = [lb.text.strip() for lb in labels]
    assert label in texts

@then('I should see the submit button "{text}"')
def step_button(context, text):
    el = context.driver.find_element(By.CSS_SELECTOR, "#form-login .btn-submit")
    assert text in el.text
    assert el.is_displayed()

@when('I fill in the email with "{email}"')
def step_email(context, email):
    el = context.driver.find_element(By.ID, "username")
    el.clear()
    el.send_keys(email)

@when('I fill in the password with "{password}"')
def step_password(context, password):
    el = context.driver.find_element(By.ID, "password")
    el.clear()
    el.send_keys(password)

@when("I click the submit button")
def step_click(context):
    context.driver.find_element(By.CSS_SELECTOR, "#form-login .btn-submit").click()

@then("I should be redirected to the dashboard page")
def step_dashboard(context):
    WebDriverWait(context.driver, 10).until(
        lambda d: "/DashboardController" in d.current_url
    )
    assert "/DashboardController" in context.driver.current_url

@then('I should see alert message "{message}"')
def step_alert(context, message):
    form = context.driver.find_element(By.ID, "form-login")

    alert = WebDriverWait(form, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger"))
    )

    text = alert.text
    assert message in text