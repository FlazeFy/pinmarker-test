from behave import then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@then('I should see the summary section title "{label}"')
def step_summary_section_title(context, label):
    section = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "summary-section"))
    )

    labelSection = section.find_element(By.CSS_SELECTOR, "h2")

    # Validate section title
    assert labelSection.text.strip() == label

@then('I should see the summary labels "{labels}"')
def step_summary_label(context, labels):
    section = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "summary-section"))
    )

    # Validate stats box label exist
    labelElements = section.find_elements(By.CSS_SELECTOR, ".stat-label")
    assert len(labelElements) > 0

    # Take and split label for each stats
    expectedLabels = [label.strip() for label in labels.split(", ")]

    actualLabels = []
    for element in labelElements:
        valueText = element.text.strip()

        # Validate place is not empty
        assert valueText != ""

        actualLabels.append(valueText)

    # Validate all expected label exist
    assert actualLabels == expectedLabels

@then('the counters should contain numeric values')
def step_summary_label(context):
    section = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "summary-section"))
    )

    # Validate stats box value exist
    pureNumericValElements = section.find_elements(By.CSS_SELECTOR, ".stat-value")
    assert len(pureNumericValElements) > 0

    for el in pureNumericValElements:
        valueText = el.text.strip()

        # Validate value is not empty
        assert valueText != ""

        # Validate value is nummeric
        assert valueText.isdigit()

    # Validate stats box value exist
    numericValWithUnitElements = section.find_elements(By.CSS_SELECTOR, ".stat-meta")
    assert len(numericValWithUnitElements) > 0

    for el in numericValWithUnitElements:
        valueText = el.text.strip()

        # Validate value is not empty
        assert valueText != ""

        # Extract numeric parts
        numericPart = valueText.split()[0]

        # Validate first val is numeric
        assert numericPart.isdigit()

    # Validate stats box value name (context value) exist
    contextValElements = section.find_elements(By.CSS_SELECTOR, ".stat-name")
    assert len(contextValElements) > 0

    for el in contextValElements:
        valueText = el.text.strip()

        # Validate value is not empty
        assert valueText != ""

        