import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import capture_network_logs, get_response_time_from_log

SLOW_THRESHOLD_MS = 5000  # 5 seconds

def generate_widget_warnings(driver):
    """
    Generate warning lines for all pre-added widgets.
    Each warning includes:
      - Widget name
      - API URL
      - Reason (slow / failed)
      - Response time or status code
    Returns list of warning lines (for WhatsApp).
    """
    warnings = []

    # Wait for board to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testing-id='Board_WidgetsContainer']"))
    )

    widgets = driver.find_elements(By.CSS_SELECTOR, "[data-testing-id^='Widgets_']")
    if not widgets:
        logging.warning("⚠ No widgets found on the board")
        return warnings

    for i, widget in enumerate(widgets, start=1):
        widget_name = widget.get_attribute("data-testing-id")
        log_file = f"network_logs/widget_{i}_{widget_name}.json"

        # Capture network logs for this widget
        capture_network_logs(driver, log_file)

        # Extract API response info
        network_data = get_response_time_from_log(log_file)

        for api in network_data:
            url = api.get("url", "unknown_url")
            status = api.get("status_code", 0)
            response_time = api.get("response_time_ms", 0)

            # Slow API warning
            if response_time > SLOW_THRESHOLD_MS:
                warnings.append(
                    f"⚠ {widget_name}: API {url} is slow ({response_time} ms)"
                )

            # Failed API warning
            if status >= 400:
                warnings.append(
                    f"⚠ {widget_name}: API {url} failed with status {status}"
                )

    return warnings
