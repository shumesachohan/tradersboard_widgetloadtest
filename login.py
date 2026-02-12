from datetime import datetime
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
from setupdriver import LoggedChromeDriver, capture_network_logs, get_chrome_options, get_response_time_from_log
from utils import findElement

# ------------------------------
# Load environment & logging
# ------------------------------
load_dotenv()
BASE_URL = os.getenv('BASE_URL')
CHAT_ID = os.getenv('CHAT_ID')
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

# ------------------------------
# Generate widget warnings
# ------------------------------

# ------------------------------
# Send WhatsApp warnings
# ------------------------------
# Thresholds
SLOW_WIDGET_THRESHOLD_SEC = 5  # warn if widget load > 5 sec
SLOW_API_THRESHOLD_MS = 5000   # warn if single API > 5 sec
def generate_widget_warnings(driver):
    """
    Detect all pre-added widgets on the board, capture backend API response times,
    including proxy payload real URLs, and return clean warning lines (no duplicates).
    """

    warnings = []

    try:
        logging.info("⏳ Waiting for board to load...")

        # Wait for board container
        board_container = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]'))
        )

        logging.info("✅ Board loaded, detecting widgets...")

        # Find all widgets
        widgets = driver.find_elements(By.CSS_SELECTOR, "[data-testing-id^='Widgets_']")
        total_widgets = len(widgets)
        logging.info(f"🟢 Total widgets detected: {total_widgets}")

        if total_widgets == 0:
            warnings.append("⚠ No widgets found on the board!")
            return warnings

        # Loop through widgets
        for i, widget in enumerate(widgets, start=1):
            widget_name = widget.get_attribute("data-testing-id")
            logging.info(f"🔹 Checking widget {i}/{total_widgets}: {widget_name}")

            log_filename = f"widget_{i}_{widget_name.replace('Widgets_', '')}"
            capture_network_logs(driver, log_filename)

            time.sleep(1)

            network_data = get_response_time_from_log(log_filename)

            if not network_data:
                continue

            api_times = {}

            for api in network_data:
                url = api.get("url", "")
                rt = api.get("response_time_ms", 0)

                if not url:
                    continue

                url_lower = url.lower()

                # 🚫 Ignore static files (JS, CSS, images, fonts)
                if url_lower.endswith((
                    ".js", ".css", ".png", ".jpg", ".jpeg",
                    ".svg", ".woff", ".woff2", ".ico", ".map"
                )):
                    continue

                # 🚫 Ignore completely external domains
                if "traderboard-dev.traderverse.io" not in url_lower:
                    continue

                # ✅ Extract real URL from proxy payload if available
                if url_lower.endswith("/proxy") or "/widgets/create" in url_lower:
                    try:
                        # payload contains real endpoint URL
                        payload_url = api.get("request_payload", {}).get("url")
                        if payload_url:
                            url = payload_url
                    except Exception:
                        pass  # fallback to proxy URL if parsing fails

                # Remove duplicates (keep max response time)
                if url not in api_times:
                    api_times[url] = rt
                else:
                    api_times[url] = max(api_times[url], rt)

            if not api_times:
                continue

            # Slowest backend API time for widget
            max_api_time_ms = max(api_times.values())

            if max_api_time_ms > SLOW_WIDGET_THRESHOLD_SEC * 1000:
                warnings.append(
                    f"⚠ Widget '{widget_name}' is slow: {round(max_api_time_ms/1000, 2)} sec"
                )

            # Individual slow API warnings
            for url, rt in api_times.items():
                if rt > SLOW_API_THRESHOLD_MS:
                    warnings.append(
                        f"⚠ Widget '{widget_name}' API slow: {url} → {round(rt/1000, 2)} sec"
                    )

        logging.info("✅ Widget check completed")
        return warnings

    except Exception as e:
        logging.error(f"❌ Error in generating widget warnings: {e}")
        warnings.append(f"❌ Error: {e}")
        return warnings

def send_widget_report_whatsapp(warnings):
    """
    Sends WhatsApp message containing only warnings
    """
    if not warnings:
        logging.info("No slow widgets detected. No WhatsApp message sent.")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    whatsapp_text = f"🧪 Tradersboard Widget Page Warnings\n🕒 {now}\n\n"
    whatsapp_text += "\n".join(warnings)

    if not CHAT_ID:
        logging.error("CHAT_ID not set. Cannot send WhatsApp message.")
        return

    send_whatsapp_message(CHAT_ID.strip(), whatsapp_text)
    logging.info("WhatsApp warnings sent.")


# ------------------------------
# Main execution
# ------------------------------
if __name__ == "__main__":
    # Test login data
    

    driver = LoggedChromeDriver(
        service=Service(ChromeDriverManager().install()),
        options=get_chrome_options()
    )
    driver.set_window_size(1920,1080)
    logging.info("✅ WebDriver ready")

    try:
        # Login
        login_success = login_user(driver, login_data)
        if login_success:
            logging.info("Login successful ✅")

            # Generate warnings for all pre-added widgets
            warnings = generate_widget_warnings(driver)

            # Send WhatsApp report
            send_widget_report_whatsapp(warnings)

        else:
            logging.error("❌ Login failed. Cannot check widgets.")

    finally:
        driver.quit()
