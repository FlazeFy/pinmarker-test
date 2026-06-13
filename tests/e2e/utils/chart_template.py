from selenium.webdriver.common.by import By

VALID_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def check_monthly_line_chart(driver, holder_id):
    holder = driver.find_element(By.CSS_SELECTOR, holder_id)
    labels = holder.find_elements(By.CSS_SELECTOR, ".apexcharts-xaxis-texts-g .apexcharts-xaxis-label tspan")
    for label in labels:
        text = label.text.strip()
        assert text in VALID_MONTHS, f"Invalid month label: '{text}'"

def check_line_chart_valid_values(driver, holder_id):
    holder = driver.find_element(By.CSS_SELECTOR, holder_id)
    data_labels = holder.find_elements(By.CSS_SELECTOR, ".apexcharts-datalabel")
    for el in data_labels:
        text = el.text.strip()
        if not text:
            continue
        val = float(text)
        assert val >= 0, f"Value {val} is less than 0"