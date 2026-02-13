import base64
import json
import logging
import datetime
import inspect
import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up logger to handle UTF-8 characters
logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)
logger = logging.getLogger("TestLogger")
logger.setLevel(logging.INFO)

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

file_handler = logging.FileHandler(f"test_log.log", encoding="utf-8")
log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

def get_chrome_options():
    """
    Returns a pre-configured Chrome Options object.
    """
    chrome_options = Options()
    # prefs = {
    #     "profile.managed_default_content_settings.images": 2,
    #     "profile.managed_default_content_settings.stylesheets": 2
    # }
    # chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-extensions")
    # options.add_argument("--auto-open-devtools-for-tabs") 
    chrome_options.add_argument("--log-level=3") 
    chrome_options.add_argument("--silent")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    return chrome_options

def get_response_body(driver, request_id):
    for _ in range(2):  # try twice
        try:
            result = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
            body = result.get("body", "")
            if result.get("base64Encoded", False):
                body = base64.b64decode(body).decode("utf-8")
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return body  # Return raw if not JSON
        except Exception as e:
            last_error = e
            time.sleep(0.5)  # brief pause
    
    if "No resource with given identifier found" in str(last_error):
        logger.debug(f"⚠️ Skipping response body for request {request_id} (resource not found)")
    else:
        logger.warning(f"Couldn't get response body for request {request_id}: {last_error}")
    
    return None
def get_response_time_from_log(log_filename):
    """
    Reads network log JSON file saved by capture_network_logs
    Returns list of dicts: url, status_code, response_time_ms, request_payload
    Extracts real API URL from proxy payload if present.
    """
    try:
        log_path = f"network_logs/{log_filename}_with_requests_and_console.json"
        if not os.path.exists(log_path):
            logging.warning(f"⚠ Log file not found: {log_path}")
            return []

        with open(log_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        network_logs = data.get("network_logs", [])
        result = []

        for entry in network_logs:
            url = entry.get("url", "Unknown")
            status = entry.get("status_code", 0)
            response_time = entry.get("response_time_ms", None)
            request_payload = entry.get("request_body", {})

            # ✅ If this is a proxy call, extract real backend URL from payload
            if "/proxy" in url and isinstance(request_payload, str):
                try:
                    payload_json = json.loads(request_payload)
                    real_url = payload_json.get("url")
                    if real_url:
                        url = real_url
                        request_payload = payload_json  # keep full payload if needed
                except Exception as e:
                    logging.warning(f"⚠ Could not parse proxy payload for {url}: {e}")

            result.append({
                "url": url,
                "status_code": status,
                "response_time_ms": response_time,
                "request_payload": request_payload
            })

        return result

    except Exception as e:
        logging.error(f"❌ Error reading network log {log_filename}: {e}")
        return []
def capture_proxy_network_logs(driver, test_name, widget_name):
    """
    Capture network logs:
    - Only proxy calls
    - Extract real URL from request payload
    - Record response time
    - Save in network_logs/<test_name>.json
    """
    try:
        if not getattr(driver, "session_id", None):
            logging.warning("⚠ Driver session not found, skipping network logs")
            return

        # Get performance logs
        logs = driver.get_log("performance")
        if not logs:
            logging.warning(f"⚠ No network logs captured for {test_name}")
            return

        request_map = {}  # request_id -> start_time & payload
        log_entries = []

        for entry in logs:
            try:
                message = json.loads(entry["message"])["message"]
                method = message.get("method", "")
                params = message.get("params", {})

                # Track requests
                if method == "Network.requestWillBeSent":
                    request_id = params.get("requestId")
                    request = params.get("request", {})
                    url = request.get("url", "")
                    post_data = request.get("postData", None)

                    # Only store proxy URLs
                    if url.endswith("/proxy") or "/widgets/create" in url:
                        request_map[request_id] = {
                            "start_time": time.perf_counter(),
                            "payload": post_data
                        }

                # Track responses
                elif method == "Network.responseReceived":
                    request_id = params.get("requestId")
                    response = params.get("response", {})
                    url = response.get("url", "")

                    if request_id in request_map:
                        start_time = request_map[request_id]["start_time"]
                        response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

                        # Extract real URL from proxy payload
                        payload_url = None
                        try:
                            payload = request_map[request_id]["payload"]
                            if payload:
                                payload_json = json.loads(payload)
                                payload_url = payload_json.get("url")
                        except:
                            pass

                        if payload_url:
                            log_entries.append({
                             "widget_name": widget_name,   # ✅ ADD THIS
                             "real_url": payload_url,
                             "proxy_url": url,
                             "response_time_ms": response_time_ms
})


                        # Remove processed request
                        request_map.pop(request_id, None)

            except Exception as e:
                logging.warning(f"⚠ Skipping a log entry due to error: {e}")
                continue

        # Save logs
        os.makedirs("network_logs", exist_ok=True)
        log_file = f"network_logs/{test_name}_proxy_only.json"
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(log_entries, f, indent=2, ensure_ascii=False)

        logging.info(f"✅ Proxy network logs saved: {log_file}")
        return log_file

    except Exception as e:
        logging.error(f"❌ Error capturing proxy network logs: {e}")
        return
          

     
def capture_logs(driver, test_name):
    """
    Capture console logs & raw network logs and save them to files.
    """
    try:
        # ✅ Console Logs
        console_logs = driver.get_log("browser")
        console_log_path = f"logs/{test_name}_console_logs.txt"
        with open(console_log_path, "w", encoding="utf-8") as file:
            for log in console_logs:
                file.write(f"[{log['level']}] {log['message']}\n")
        logger.info(f"✅ Console logs saved: {console_log_path}")

        # ✅ Raw Network Logs
        network_logs = driver.get_log("performance")
        network_log_path = f"logs/{test_name}_network_logs.json"
        with open(network_log_path, "w", encoding="utf-8") as file:
            json.dump(network_logs, file, indent=4)
        logger.info(f"✅ Raw network logs saved: {network_log_path}")

    except Exception as e:
        logger.error(f"❌ Error capturing logs: {e}")
class LoggedChromeDriver(webdriver.Chrome):
    # def __init__(self, *args, **kwargs):
    #     self._test_name = self._get_test_name()
    #     super().__init__(*args, **kwargs)
    #     self.execute_cdp_cmd("Network.enable", {})  # ✅ Enable Network domain
    #     logger.info(f"🚀 Starting test: {self._test_name}")
    #     capture_logs(self, f"{self._test_name}_start")

  
    def _get_test_name(self):
        stack = inspect.stack()
        for frame in stack:
            if frame.function.startswith("test_"):
                return frame.function
        return "unnamed_test"
    
    def clear_network_logs(self):
        self.network_logs.clear()
        self.console_logs.clear()

    def quit(self):
        logger.info(f"🧪 Ending test: {self._test_name}")
        capture_logs(self, f"{self._test_name}_end")
        time.sleep(10)  # Give Chrome time to flush logs
        capture_proxy_network_logs(self, f"{self._test_name}_final")
        capture_logs(self, f"{self._test_name}_end")
        super().quit()


def rotate_logs():
    """
    Archives the old logs if there are more than 100 log files.
    """
    log_folder = "logs"
    archived_folder = "archived_logs"
    os.makedirs(archived_folder, exist_ok=True)

    log_files = [f for f in os.listdir(log_folder) if os.path.isfile(os.path.join(log_folder, f))]
    
    if len(log_files) > 100:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir = os.path.join(archived_folder, f"archive_{timestamp}")
        os.makedirs(archive_dir, exist_ok=True)

        for log_file in log_files:
            shutil.move(os.path.join(log_folder, log_file), archive_dir)

        logger.info(f"✅ Archived old logs to {archive_dir}")