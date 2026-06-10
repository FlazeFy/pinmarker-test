from behave import given, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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

@then('I should see the labels "{labels}"')
def step_main_category_labels(context, labels):
    section = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "main-category-section"))
    )

    expectedLabels = [label.strip() for label in labels.split(",")]
    labelElements = section.find_elements(By.CSS_SELECTOR, ".mini-label")
    actualLabels = [element.text.strip() for element in labelElements]

    # Validate label are exists
    for expectedLabel in expectedLabels:
        assert expectedLabel in actualLabels

@then("I should see the value for each main category distribution")
def step_main_category_values(context):
    section = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "main-category-section"))
    )

    valueElements = section.find_elements(By.CSS_SELECTOR, ".mini-val")

    assert len(valueElements) > 0

    for element in valueElements:
        valueText = element.text.strip()

        # Validate place is not empty and contain "Places"
        assert valueText != ""
        assert "Places" in valueText

        # Validate total places is valid number
        totalPlaces = int(valueText.replace("Places", "").strip())
        assert totalPlaces >= 0