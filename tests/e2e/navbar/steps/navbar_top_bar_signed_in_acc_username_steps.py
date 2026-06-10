from behave import given, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Utils
from tests.e2e.utils.auth_template import login

testData = {
    "email": "jalanjalan",
    "password": "admin"
}

@given("I have already signed in to the app")
def step_login(context):
    context.driver = webdriver.Chrome()
    login(context.driver, testData["email"], testData["password"])

@then('I should see my username in the navigation bar')
def step_find_signed_account_identity(context):
    section = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "top-nav-bar"))
    )

    usernameElement = section.find_element(By.ID,"username-top-bar-text")
    usernameText = usernameElement.text.strip()

    assert usernameText != ""
    assert usernameText == testData["email"]

   
