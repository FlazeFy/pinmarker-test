from behave import given
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

# Utils
from tests.e2e.utils.auth_template import login

@given("I have already signed in to the app")
def step_login(context):
    testData = {
        "email": "jalanjalan",
        "password": "admin"
    }

    context.driver = webdriver.Chrome()
    login(context.driver, testData["email"], testData["password"])