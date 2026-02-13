from datetime import datetime
import json
import os
import time
import logging
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from report import send_whatsapp_message
from setupdriver import LoggedChromeDriver, capture_proxy_network_logs, get_chrome_options
from utils import findElement, log_test_result

# ------------------------------
# Load environment & logging
# ------------------------------
load_dotenv()
BASE_URL = os.getenv('BASE_URL')
CHAT_ID = os.getenv('CHAT_ID')
ERROR_CHAT_ID = os.getenv('ERROR_CHAT_ID')

SLOW_THRESHOLD_SECONDS = 5  # warning threshold

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ------------------------------
# Login function
# ------------------------------
login_data = {
        "email":"afsheeniqbalc@gmail.com",
        "password":"Abc1234@"
    }
def login_user(driver, item):
    try:
        driver.get(BASE_URL)
        logging.info("Enter email")
        time.sleep(2)
        email = findElement(driver,'id','username')
        time.sleep(3)
        email.send_keys(item['email'])

        logging.info("Enter password")
        password = findElement(driver,'id','password')
        password.send_keys(item['password'])

        logging.info("Click login")
        login_btn = findElement(driver,'id','kc-login')
        login_btn.click()
        return True
    except Exception as e:
        logging.error(f"Login failed for {item['email']}: {e}")
        return False
SLOW_WIDGET_THRESHOLD_SEC = 5  # warn if widget load > 5 sec
SLOW_API_THRESHOLD_MS = 5000   # warn if single API > 5 sec
def generate_widget_api_lists(driver):
    warnings_list = []
    normal_list = []

    logging.info("⏳ Detecting widgets and capturing proxy API logs...")
    widgets = driver.find_elements(By.CSS_SELECTOR, "[data-testing-id^='Widgets_']")
    total_widgets = len(widgets)
    logging.info(f"🟢 Total widgets detected: {total_widgets}")

    for i, widget in enumerate(widgets, start=1):
        widget_name = widget.get_attribute("data-testing-id")
        logging.info(f"🔹 Capturing proxy API logs for widget: {widget_name}")

        # Capture proxy network logs for this widget
        test_name = f"widget_{i}_{widget_name}"
        log_file = capture_proxy_network_logs(driver, test_name, widget_name)


        # Load captured logs
        entries_data = []
        if log_file and os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                entries_data = json.load(f)  # list of dicts: real_url, proxy_url, response_time_ms

        for api in entries_data:
            real_url = api.get("real_url")
            rt_ms = api.get("response_time_ms", 0)

            line = f"{widget_name} | {real_url} | {round(rt_ms/1000,2)} sec"
            if rt_ms/1000 > SLOW_WIDGET_THRESHOLD_SEC:
                warnings_list.append(f"⚠ {line}")
            else:
                normal_list.append(f"✅ {line}")

    logging.info("✅ Widget API measurement completed")
    return warnings_list, normal_list
 
# ------------------------------
# Send WhatsApp messages
# ------------------------------
# def send_widget_whatsapp_messages(warnings_list, normal_list):
#     now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
#     try:
#         if warnings_list:
#             msg_warnings = f"🧪 Tradersboard Widget Warnings\n🕒 {now}\n\n" + "\n".join(warnings_list)
#             send_whatsapp_message(ERROR_CHAT_ID, msg_warnings)
#             logging.info(f"✅ WhatsApp warnings sent to {ERROR_CHAT_ID}")
#     except Exception as e:
#         logging.error(f"❌ Failed to send warnings WhatsApp: {e}")

#     try:
#         if normal_list:
#             msg_normal = f"🟢 Tradersboard All Widget APIs\n🕒 {now}\n\n" + "\n".join(normal_list)
#             send_whatsapp_message(CHAT_ID, msg_normal)
#             logging.info(f"✅ WhatsApp normal APIs sent to {CHAT_ID}")
#     except Exception as e:
#         logging.error(f"❌ Failed to send normal APIs WhatsApp: {e}")
# import json
# import logging
# from datetime import datetime
# from report import send_whatsapp_message
# import os

# SLOW_WIDGET_THRESHOLD_SEC = 5  # 5 sec se zyada → warning

# def parse_proxy_logs_and_send_whatsapp(log_file_path, chat_id, error_chat_id):
#     """
#     Reads proxy-only network logs and sends two WhatsApp messages:
#     1️⃣ Warnings → widgets with API response > threshold
#     2️⃣ Normal → all other APIs
#     Format:
#       WidgetName | API Real URL | Response Time
#     """
#     if not os.path.exists(log_file_path):
#         logging.error(f"❌ Proxy log file not found: {log_file_path}")
#         return

#     # Load proxy network logs
#     with open(log_file_path, "r", encoding="utf-8") as f:
#         logs = json.load(f)

#     warnings_list = []
#     normal_list = []

#     for entry in logs:
#         widget_name = entry.get("widget_name", "Unknown_Widget")
#         real_url = entry.get("real_url", "Unknown_URL")
#         response_time_ms = entry.get("response_time_ms", 0)

#         line = f"{widget_name} | {real_url} | {round(response_time_ms/1000, 2)} sec"

#         if response_time_ms/1000 > SLOW_WIDGET_THRESHOLD_SEC:
#             warnings_list.append(f"⚠ {line}")
#         else:
#             normal_list.append(f"✅ {line}")

#     now = datetime.now().strftime("%Y-%m-%d %H:%M")

#     # Send warnings message
#     if warnings_list:
#         msg_warnings = f"🧪 Tradersboard Widget Warnings\n🕒 {now}\n\n" + "\n".join(warnings_list)
#         send_whatsapp_message(error_chat_id.strip(), msg_warnings)
#         logging.info("✅ WhatsApp warnings sent")

#     # Send normal APIs message
#     if normal_list:
#         msg_normal = f"🟢 Tradersboard All Widget APIs\n🕒 {now}\n\n" + "\n".join(normal_list)
#         send_whatsapp_message(chat_id.strip(), msg_normal)
#         logging.info("✅ WhatsApp normal APIs sent")

#     logging.info("✅ WhatsApp messages completed")
def parse_proxy_logs_and_send_whatsapp(log_file_path, chat_id, error_chat_id):
    """
    Reads proxy-only network logs and sends two WhatsApp messages:
    1️⃣ Warnings → APIs with response > threshold
    2️⃣ Normal → all other APIs
    Format:
      API Real URL | Response Time (sec + ms)
    """
    if not os.path.exists(log_file_path):
        logging.error(f"❌ Proxy log file not found: {log_file_path}")
        return

    # Load proxy network logs
    with open(log_file_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    warnings_list = []
    normal_list = []

    for entry in logs:
        real_url = entry.get("real_url", "Unknown_URL")
        response_time_ms = entry.get("response_time_ms", 0)

        # Compute both sec and ms
        response_sec = round(response_time_ms / 1000, 2)
        response_ms = round(response_time_ms, 2)

        line = f"{real_url} | {response_sec} sec | {response_ms} ms"

        if response_sec > SLOW_WIDGET_THRESHOLD_SEC:
            warnings_list.append(f"⚠ {line}")
        else:
            normal_list.append(f"✅ {line}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Send warnings message
    if warnings_list:
        msg_warnings = f"🧪 Tradersboard Widget Warnings\n🕒 {now}\n\n" + "\n".join(warnings_list)
        send_whatsapp_message(ERROR_CHAT_ID.strip(), msg_warnings)
        logging.info("✅ WhatsApp warnings sent")

    # Send normal APIs message
    if normal_list:
        msg_normal = f"🟢 Tradersboard All Widget APIs\n🕒 {now}\n\n" + "\n".join(normal_list)
        send_whatsapp_message(CHAT_ID.strip(), msg_normal)
        logging.info("✅ WhatsApp normal APIs sent")

    logging.info("✅ WhatsApp messages completed")

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
        # ------------------
        # Login
        # ------------------
        success = login_user(driver, login_data)
        if not success:
            logging.error("❌ Login failed. Exiting script.")
            driver.quit()
            exit(1)

        logging.info("✅ Logged in successfully")
        time.sleep(3)  # wait for board to load

        # ------------------
        # Generate widget API lists
        # ------------------
        warnings, normal = generate_widget_api_lists(driver)

        # ------------------
        # Send WhatsApp messages
        # ------------------
        # send_widget_whatsapp_messages(warnings, normal)
        log_file = "network_logs/unnamed_test_final_proxy_only.json"
        parse_proxy_logs_and_send_whatsapp(log_file, CHAT_ID, ERROR_CHAT_ID)
        
    finally:
        driver.quit()
        logging.info("✅ Driver closed")
