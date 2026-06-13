from behave import then
from selenium.webdriver.common.by import By
from tests.e2e.utils.chart_template import check_line_chart_valid_values, check_monthly_line_chart

chart_holder = "#line_total_visit_per_month"

@then('I should see the total visit monthly section title "{title}"')
def step_see_section_title(context, title):
    el = context.driver.find_element(By.CSS_SELECTOR, "#total_visit_monthly-section h2")
    assert title in el.text, f"Expected '{title}' in '{el.text}'"

@then("I should see the line chart and the horizontal label showing the list of month names")
def step_see_monthly_line_chart(context):
    check_monthly_line_chart(context.driver, chart_holder)

@then("I should see a chart with valid values for each series")
def step_see_chart_valid_values(context):
    check_line_chart_valid_values(context.driver, chart_holder)