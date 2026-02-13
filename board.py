import os
import time
import json
import logging
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from setupdriver import LoggedChromeDriver, get_chrome_options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from report import send_whatsapp_message

# ------------------------------
# Config
# ------------------------------
BASE_URL = os.getenv("BASE_URL")
CHAT_ID = os.getenv("CHAT_ID")
SLOW_THRESHOLD_MS = 5000  # 5 sec in ms

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

# ------------------------------
# Capture only proxy network logs
# ------------------------------
def capture_proxy_network_logs(driver, test_name):
    """
    Capture only proxy APIs and their response time from network logs.
    Returns a list of dicts: [{"widget": widget_name, "api": real_url, "response_time_ms": rt}]
    """
    logs = driver.get_log("performance")
    if not logs:
        logging.warning("⚠ No network logs captured")
        return []

    request_map = {}  # requestId -> start_time & payload
    captured_entries = []

    for entry in logs:
        try:
            message = json.loads(entry["message"])["message"]
            method = message.get("method", "")
            params = message.get("params", {})

            if method == "Network.requestWillBeSent":
                request_id = params.get("requestId")
                request = params.get("request", {})
                url = request.get("url", "")
                post_data = request.get("postData", None)

                if url.endswith("/proxy") or "/widgets/create" in url:
                    request_map[request_id] = {
                        "start_time": time.perf_counter(),
                        "payload": post_data,
                        "proxy_url": url
                    }

            elif method == "Network.responseReceived":
                request_id = params.get("requestId")
                response = params.get("response", {})
                url = response.get("url", "")

                if request_id in request_map:
                    start_time = request_map[request_id]["start_time"]
                    response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

                    payload_url = None
                    try:
                        payload = request_map[request_id]["payload"]
                        if payload:
                            payload_json = json.loads(payload)
                            payload_url = payload_json.get("url")
                    except:
                        pass

                    if payload_url:
                        captured_entries.append({
                            "proxy_url": request_map[request_id]["proxy_url"],
                            "real_url": payload_url,
                            "response_time_ms": response_time_ms
                        })

                    request_map.pop(request_id, None)
        except:
            continue

    # Save to file
    os.makedirs("network_logs", exist_ok=True)
    file_path = f"network_logs/{test_name}_proxy_only.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(captured_entries, f, indent=2, ensure_ascii=False)

    logging.info(f"✅ Proxy network logs saved: {file_path}")
    return captured_entries

# ------------------------------
# Generate widget API warnings & normal lists
# ------------------------------
def generate_widget_api_lists(driver):
    """
    Returns two lists:
    - warnings_list → APIs > 5 sec
    - normal_list → APIs <= 5 sec
    """
    warnings_list = []
    normal_list = []

    # Wait for board
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testing-id^='Widgets_']"))
    )
    widgets = driver.find_elements(By.CSS_SELECTOR, "[data-testing-id^='Widgets_']")
    logging.info(f"🟢 Total widgets detected: {len(widgets)}")

    for i, widget in enumerate(widgets, start=1):
        widget_name = widget.get_attribute("data-testing-id")
        logging.info(f"🔹 Capturing proxy API logs for widget: {widget_name}")

        # Capture network logs for this widget
        test_name = f"widget_{i}_{widget_name}"
        entries = capture_proxy_network_logs(driver, test_name)

        for api in entries:
            real_url = api.get("real_url")
            rt_ms = api.get("response_time_ms", 0)

            line = f"{widget_name} | {real_url} | {round(rt_ms/1000,2)} sec"
            if rt_ms > SLOW_THRESHOLD_MS:
                warnings_list.append(f"⚠ {line}")
            else:
                normal_list.append(f"✅ {line}")

    logging.info("✅ Widget API measurement completed")
    return warnings_list, normal_list

# ------------------------------
# Send WhatsApp messages
# ------------------------------
def send_widget_whatsapp_messages(warnings_list, normal_list):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if warnings_list:
        msg_warnings = f"🧪 Tradersboard Widget Warnings\n🕒 {now}\n\n" + "\n".join(warnings_list)
        send_whatsapp_message(CHAT_ID.strip(), msg_warnings)
        logging.info("✅ WhatsApp warnings sent")

    if normal_list:
        msg_normal = f"🟢 Tradersboard Normal Widget APIs\n🕒 {now}\n\n" + "\n".join(normal_list)
        send_whatsapp_message(CHAT_ID.strip(), msg_normal)
        logging.info("✅ WhatsApp normal APIs sent")

# ------------------------------
# Full flow
# ------------------------------
if __name__ == "__main__":
    driver = LoggedChromeDriver(
        service=Service(ChromeDriverManager().install()),
        options=get_chrome_options()
    )
    driver.set_window_size(1920, 1080)

    try:
        # Login
        driver.get(BASE_URL)
        logging.info("✅ Logged in successfully")

        # Generate lists
        warnings, normal = generate_widget_api_lists(driver)

        # Send WhatsApp messages
        send_widget_whatsapp_messages(warnings, normal)

    finally:
        driver.quit()
        logging.info("✅ Driver closed")
