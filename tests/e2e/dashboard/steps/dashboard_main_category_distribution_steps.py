from behave import then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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