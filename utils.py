import json
import os
import time
from venv import logger
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from pathlib import Path
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException ,ElementClickInterceptedException
test_results = []


widget_video_filename = "widget_test_run.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = None
def select_variant_value_brand(driver, field_element, value):
    try:
        # Click on the dropdown field to activate the input
        ActionChains(driver).move_to_element(field_element).click().perform()

        # Wait for the input field to appear after click
        input_xpath = "//input[starts-with(@id, 'react-select') and contains(@id, '-input')]"
        input_field = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, input_xpath))
        )

        input_field.clear()
        input_field.send_keys(value)
        time.sleep(0.5)  # Let dropdown options load
        input_field.send_keys(Keys.RETURN)

        logger.info(f"Selected value '{value}' for element {field_element}")
    except Exception as e:
        logger.error(f"Failed to select variant value '{value}': {e}")



def get_by_attribute(driver, attribute_name, attribute_value):
    return driver.find_element(By.XPATH, f"//*[@{attribute_name}='{attribute_value}']")


def save_local_storage(driver, file_name):
    """Save browser local storage to a file."""
    try:
        local_storage = driver.execute_script("return window.localStorage;")
        with open(file_name, 'w') as f:
            json.dump(dict(local_storage), f)
        logging.info(f"Local storage data saved to {file_name}")
    except Exception as e:
        logging.error(f"Failed to save local storage: {e}")
def log_test_result(test_name, provided_data, expected_output, actual_output, exc_info=False, message=None): 
    """
    Logs the test result in a structured format and stores it for report generation.
    """
    result = "Pass" if expected_output == actual_output else "Fail"

    log_message = (
        f"Test Name: {test_name}\n"
        f"Provided Data: {json.dumps(provided_data, indent=4)}\n"
        f"Expected Output: {expected_output}\n"
        f"Actual Output: {actual_output}\n"
        f"Result: {result}\n"
        + "\n" + "-"*40 + "\n"
    )

    if result == "Fail" and exc_info:
        logging.error(log_message, exc_info=True)
    else:
        logging.info(log_message)

    # Append to test_results for the report
    test_results.append({
        "name": test_name,
        "status": result.upper(),
        "provided_data": provided_data,
        "expected": expected_output,
        "actual": actual_output,
        "message": message or actual_output  # <-- THIS LINE ADDS MESSAGE
    })
        
def single_test_logger(test_name,description,expected_output,result):
    print(f"{test_name}-{description}:Expected_Output {expected_output},Actual_Output:{result}")

def overall_test_logger(test_name,total,failed,passed):
    print(f"{test_name}-total:{total},passed:{passed},failed:{failed}")
        
        
def capture_screenshot(driver, file_name="screenshot.png"):
    """
    Captures a screenshot of the current browser window.
    """
    try:
        file_path = os.path.join(os.getcwd(), file_name)
        driver.save_screenshot(file_path)
        logging.info(f"Screenshot saved at {file_path}")
    except Exception as e:
        logging.error(f"Failed to capture screenshot: {e}")
        
        
def clear_and_input_text(element, text):
    """
    Clears an input field and types new text.
    """
    try:
        element.clear()
        element.send_keys(text)
        logging.info(f"Input text '{text}' into the field.")
    except Exception as e:
        logging.error(f"Failed to input text: {e}")
        raise
def click_if_visible(driver, attribute_name, attribute_value, timeout=10):
    try:
        # Wait for visibility
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, f"//*[@{attribute_name}='{attribute_value}']"))
        )

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

        # Get bounding rect before clicking
        rect = driver.execute_script("""
            var rect = arguments[0].getBoundingClientRect();
            return {x: rect.x, y: rect.y, width: rect.width, height: rect.height};
        """, element)
        logging.info(f"Element position and size: {rect}")

        # Click via JS
        driver.execute_script("arguments[0].click();", element)
        logging.info(f"Clicked element [{attribute_name}='{attribute_value}'] via JS.")
        return element

    except Exception as e:
        logging.error(f"Failed to click element [{attribute_name}='{attribute_value}']: {e}")
        return None
    
    
def select_brand_category(driver, value, timeout=10):
    try:
        # Step 1: Scroll and click on the dropdown wrapper
        dropdown_wrapper = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testing-id='brandcategory_brandInfo']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_wrapper)
        ActionChains(driver).move_to_element(dropdown_wrapper).click().perform()

        # Step 2: Wait for the actual input field inside the dropdown
        input_field = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "react-select-6-input"))
        )
        input_field.send_keys(value)
        time.sleep(0.5)  # Small wait for options to load
        input_field.send_keys(Keys.ENTER)

        logger.info(f"Brand category '{value}' selected successfully.")

    except Exception as e:
        logger.error(f"Failed to select brand category '{value}': {e}")    
    
def select_variant_value2(driver, value, timeout=10):
    try:
        # Find input field inside React Select
        input_field = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//input[starts-with(@id, 'react-select') and contains(@id, '-input')]"))
        )
        input_field.clear()  # optional for safety
        input_field.send_keys(value)
        time.sleep(0.5)
        input_field.send_keys(Keys.RETURN)
        logger.info(f"Selected variant value: {value}")
    except Exception as e:
        logger.error(f"Failed to select variant value '{value}': {e}")

    
def select_variant_value(driver, value):
    try:
        input_field = driver.find_element(By.XPATH, "//input[starts-with(@id, 'react-select') and contains(@id, '-input')]")
        input_field.send_keys(value)
        time.sleep(0.5)
        input_field.send_keys(Keys.RETURN)
        logger.info(f"Selected variant value: {value}")
    except Exception as e:
        logger.error(f"Failed to select variant value '{value}': {e}")
    
    
def wait_for_page_load(driver, timeout=10):
    """
    Waits for the page to fully load by monitoring the document.readyState.
    """
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        logging.info("Page loaded successfully.")
    except Exception as e:
        logging.error(f"Page did not load within {timeout} seconds: {e}")
        raise
def validate_text_on_page(driver, text):
    """
    Validates if the given text is present on the current page.
    """
    try:
        if text in driver.page_source:
            logging.info(f"Text '{text}' found on the page.")
            return True
        else:
            logging.warning(f"Text '{text}' not found on the page.")
            return False
    except Exception as e:
        logging.error(f"Error while validating text: {e}")
        raise
def execute_js(driver, script, *args):
    """
    Executes JavaScript in the browser context.
    """
    try:
        result = driver.execute_script(script, *args)
        logging.info(f"Executed script: {script}")
        return result
    except Exception as e:
        logging.error(f"Failed to execute JavaScript: {e}")
        raise

def highlight_element(driver, element, duration=2):
    """
    Highlights a WebElement by changing its style temporarily.
    """
    try:
        original_style = element.get_attribute("style")
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            "border: 2px solid red; background-color: yellow;",
        )
        time.sleep(duration)
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            original_style,
        )
        logging.info("Element highlighted.")
    except Exception as e:
        logging.error(f"Failed to highlight element: {e}")
def retry(action, retries=3, delay=2):
    """
    Retries a specified action in case of failure.
    """
    for attempt in range(1, retries + 1):
        try:
            return action()
        except Exception as e:
            logging.warning(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                logging.error(f"Action failed after {retries} retries.")
                raise
def handle_alert(driver, action="accept"):
    """
    Handles browser alerts by accepting or dismissing them.
    """
    try:
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        if action == "accept":
            alert.accept()
            logging.info("Alert accepted.")
        elif action == "dismiss":
            alert.dismiss()
            logging.info("Alert dismissed.")
        else:
            logging.error("Invalid action for alert. Use 'accept' or 'dismiss'.")
    except Exception as e:
        logging.error(f"No alert found or failed to handle alert: {e}")

    
def switch_to_frame(driver, locator_type, locator_value):
    """
    Switches to a specified iframe by locator.
    """
    try:
        frame = driver.find_element(locator_type, locator_value)
        driver.switch_to.frame(frame)
        logging.info("Switched to the iframe.")
    except Exception as e:
        logging.error(f"Failed to switch to iframe: {e}")
        raise
    
    
def wait_for_element_to_disappear(driver, locator_type, locator_value, timeout=10):
    """
    Waits for an element to disappear from the page.
    """
    try:
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((locator_type, locator_value))
        )
        logging.info("Element disappeared.")
    except Exception as e:
        logging.error(f"Element did not disappear within {timeout} seconds: {e}")
        raise
    
    
def scroll_and_find(driver, find_function):
    """
    Scrolls to the element and ensures it is visible.
    :param driver: WebDriver instance
    :param find_function: A lambda function to locate the element
    :return: The WebElement after ensuring visibility
    """
    element = WebDriverWait(driver, 10).until(find_function)  
    driver.execute_script("arguments[0].scrollIntoView(true);", element)  # Scroll into view
    ActionChains(driver).move_to_element(element).perform()  # Ensure focus
    return element

def get_by_attribute(driver, attribute_name, attribute_value):
    return driver.find_element("css selector", f"[{attribute_name}='{attribute_value}']")

def log_failure(log_file, attribute_name, attribute_value, reason):
    os.makedirs("unfound_elements", exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] @{attribute_name}='{attribute_value}' - {reason}\n")

def findElement(driver, attribute_name, attribute_value, timeout=20, try_click=False):
    start_time = time.time()
    try:
        elem = WebDriverWait(driver, timeout, 0.5).until(
            lambda d: get_by_attribute(d, attribute_name, attribute_value)
        )
        if try_click:
            try:
                elem.click()
            except ElementClickInterceptedException as e:
                log_failure("unfound_elements/missing_elements.csv", attribute_name, attribute_value, f"Click Intercepted: {str(e).splitlines()[0]}")
        return elem
    except TimeoutException:
        if time.time() - start_time >= 5:
            log_failure("unfound_elements/missing_elements.csv", attribute_name, attribute_value, "Not found in 5s")
        return None

def scroll_and_find_by_attribute(driver, attribute_name, attribute_value, timeout=10, try_click=False):
    start_time = time.time()
    try:
        element = WebDriverWait(driver, timeout, 0.1).until(
            lambda d: get_by_attribute(d, attribute_name, attribute_value)
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        ActionChains(driver).move_to_element(element).perform()
        if try_click:
            try:
                element.click()
            except ElementClickInterceptedException as e:
                log_failure("unfound_elements/missing_elements.csv", attribute_name, attribute_value, f"Click Intercepted: {str(e).splitlines()[0]}")
        return element
    except TimeoutException:
        if time.time() - start_time >= 5:
            log_failure("unfound_elements/missing_elements.csv", attribute_name, attribute_value, "Not found in 5s")
        return None

# Example usage with click handling
def click_element(driver, attribute_name, attribute_value):
    element = findElement(driver, attribute_name, attribute_value)
    if element:
        try:
            element.click()
        except ElementClickInterceptedException as e:
            logging.error(f"Click intercepted: {e}")
            # Optionally retry or scroll again
    else:
        logging.error(f"Element not found to click: @{attribute_name}='{attribute_value}'")


def wait_for_dropdown_to_close(driver, listbox_id, next_input_id):
    try:
        WebDriverWait(driver, 5, 0.5).until_not(
            EC.presence_of_element_located((By.ID, listbox_id))
        )
        WebDriverWait(driver, 5, 0.5).until(
            EC.element_to_be_clickable((By.ID, next_input_id))
        )
    except TimeoutException:
        logging.warning(f"Dropdown '{listbox_id}' did not close or next input '{next_input_id}' not clickable in time.")

        
        
def scroll_into_view_and_focus(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        ActionChains(driver).move_to_element(element).pause(0.1).perform()
    except Exception as e:
        logging.warning(f"Scroll/focus failed: {e}")


def upload_file_with_timeout_check(input_elem, file_path, timeout_threshold=5, log_path=None):
    """
    Uploads a file and logs a warning if upload takes longer than timeout_threshold seconds.
    
    Args:
        input_elem: The input[type='file'] WebElement
        file_path: Absolute path to the file to upload
        timeout_threshold: Time in seconds after which a warning should be triggered
        log_path: (Optional) CSV file to record slow uploads
    """
    try:
        start = time.time()
        input_elem.send_keys(file_path)
        duration = time.time() - start

        logging.info(f"Uploaded file: {file_path} in {duration:.2f} seconds")

        if duration > timeout_threshold:
            warning_msg = f"File upload took too long: {duration:.2f}s for {file_path}"
            logging.warning(warning_msg)

            # Optional: save to CSV
            if log_path:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(f"{file_path},{duration:.2f},Upload Delay > {timeout_threshold}s\n")

    except Exception as e:
        logging.error(f"File upload failed: {str(e)}")
        
        
  
def start_video_writer(size=(1280, 720)):
    global video_writer
    video_writer = cv2.VideoWriter(widget_video_filename, fourcc, 1.0, size)

def stop_video_writer():
    global video_writer
    if video_writer:
        video_writer.release()
        logging.info(f"Video saved as {widget_video_filename}")
        


def get_resource_path(filename):
    base_path = Path(__file__).parent
    resource_path = base_path / "resources" / filename
    return str(resource_path.resolve())
        
        
        
def wait_for_category_in_response(logs, category_name, timeout=10):
    import time
    start = time.time()
    while time.time() - start < timeout:
        for log in logs:
            if (
                "Mobiles & Tablets" in str(log.get("message", ""))
                and '"isDeleted":false' in str(log.get("message", ""))
            ):
                return True
        time.sleep(1)
    raise Exception(f"Category '{category_name}' not found in network logs")
        

def capture_browser_frame(driver):
    global video_writer
    if video_writer:
        png = driver.get_screenshot_as_png()
        frame = cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR)
        frame = cv2.resize(frame, (1280, 720))
        video_writer.write(frame)      
     
def select_from_dropdown(driver, input_box, value_to_select):
    input_box.click()
    input_box.clear()
    input_box.send_keys(value_to_select)

    # Wait for dropdown options (anywhere in the DOM)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, f"//div[contains(@class, '-option') and contains(text(), '{value_to_select}')]"))
        )
    except:
        raise Exception(f"No dropdown options found for '{value_to_select}'")

    options = driver.find_elements(By.XPATH, f"//div[contains(@class, '-option')]")
    found = False
    for option in options:
        if option.text.strip().lower() == value_to_select.strip().lower():
            driver.execute_script("arguments[0].scrollIntoView(true);", option)
            option.click()
            found = True
            break

    if not found:
        raise Exception(f"Dropdown value '{value_to_select}' not found in options.")

    # Give React some time to update the UI
    time.sleep(0.5)

    # Validate selection
    selected_value = input_box.get_attribute("value").strip().lower()
    if selected_value != value_to_select.strip().lower():
        raise Exception(f"Dropdown value '{value_to_select}' not selected properly. Got '{selected_value}'")

def set_ion_date(driver, testing_id, day, month, year):
    wait = WebDriverWait(driver, 10)

    # 1. Open the date picker
    date_input = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//ion-datetime[@data-testing-id='{testing_id}']")
    ))
    date_input.click()

    # 2. Select Day
    day_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//button[normalize-space(text())='{day}']")
    ))
    day_btn.click()

    # 3. Select Month
    month_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//button[normalize-space(text())='{month:02d}']")
    ))
    month_btn.click()

    # 4. Select Year
    year_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//button[normalize-space(text())='{year}']")
    ))
    year_btn.click()

    # 5. Click DONE
    done_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[normalize-space(text())='DONE']")
    ))
    done_btn.click()



def select_date(driver, day, month, year):
        wait = WebDriverWait(driver, 10)

        # Click the Day
        day_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space(text())='{day}']")))
        day_btn.click()

        # Click the Month
        month_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space(text())='{month:02d}']")))
        month_btn.click()

        # Click the Year
        year_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space(text())='{year}']")))
        year_btn.click()

        # Finally click DONE
        done_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='DONE']")))
        done_btn.click()
        

def set_zoom(driver, percent: int):
    """
    Set browser zoom level (shrink/enlarge font + UI).
    :param driver: Selenium WebDriver instance
    :param percent: Zoom percentage (e.g. 80 for 80%)
    """
    try:
        zoom_value = f"{percent}%"
        driver.execute_script(f"document.body.style.zoom='{zoom_value}'")
        print(f"✅ Zoom set to {zoom_value}")
        return True
    except Exception as e:
        print(f"❌ Failed to set zoom: {e}")
        return False
def wait_for_test_list_and_select(driver,item):
    try:
    # Wait for the dropdown to be clickable
        select_dropdown = findElement(driver,'data-testing-id','SelectSearch')
        select_dropdown.click()

    # Wait until the option 'Test List' becomes available in the dropdown
        WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//option[normalize-space()='test list']"))
    )
         
        

    # Click the 'Test List' option once it becomes available
        time.sleep(5)
        test_listoption = driver.find_element(By.XPATH, "//option[normalize-space()='test list']")
        test_listoption.click()
        print("Test List option selected")
        return True
    except Exception as e:
         logging.error(f"Error in notification: {e}")

def scroll_and_find_by_xpath(driver, xpath, timeout=10):
    """
    Scrolls to an element located by XPath and returns it.
    """
    try:
        # Wait for presence in DOM
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

        # Extra wait to stabilize
        WebDriverWait(driver, timeout).until(
            EC.visibility_of(element)
        )

        logging.info(f"✅ Found element by XPath: {xpath}")
        return element
    except Exception as e:
        logging.error(f"❌ scroll_and_find_by_xpath failed: {e}")
        return None
def scroll_a_little(driver, pixels=300):
    """
    Scrolls the page a small amount vertically.
    +pixels = scroll down
    -pixels = scroll up
    """
    try:
        driver.execute_script(f"window.scrollBy(0, {pixels});")
        logging.info(f"⬇️ Scrolled {pixels}px")
        time.sleep(0.5)  # give UI time to update
        return True
    except Exception as e:
        logging.error(f"❌ scroll_a_little failed: {e}")
        return False
def horizontal_scroll(driver, pixels=300):
    """
    Scrolls horizontally by a specific number of pixels.
    +pixels = scroll right
    -pixels = scroll left
    """
    try:
        driver.execute_script(f"window.scrollBy({pixels}, 0);")
        logging.info(f"✅ Scrolled horizontally by {pixels}px")
        time.sleep(0.5)
        return True
    except Exception as e:
        logging.error(f"❌ horizontal_scroll failed: {e}")
        return False
    
def scroll_and_find_by_attribute_horizontally_scrolling(driver, attribute_name, attribute_value, timeout=10, try_click=False):
    """
    Scrolls both vertically and horizontally (for edge elements)
    and returns the element if found. Works well in headless mode too.
    """
    start_time = time.time()
    try:
        # Wait for the element to appear
        element = WebDriverWait(driver, timeout, 0.2).until(
            lambda d: get_by_attribute(d, attribute_name, attribute_value)
        )

        # Scroll vertically & horizontally into view
        driver.execute_script("""
            arguments[0].scrollIntoView({
                behavior: 'smooth',
                block: 'center',
                inline: 'center'
            });
        """, element)

        # In headless mode, hover actions can fail — so only perform safely
        try:
            ActionChains(driver).move_to_element(element).perform()
        except Exception:
            logging.debug("⚠️ Skipping hover (headless mode or restricted viewport)")

        # Optionally click the element
        if try_click:
            try:
                element.click()
            except ElementClickInterceptedException as e:
                log_failure(
                    "unfound_elements/missing_elements.csv",
                    attribute_name,
                    attribute_value,
                    f"Click Intercepted: {str(e).splitlines()[0]}"
                )
        return element

    except TimeoutException:
        if time.time() - start_time >= 5:
            log_failure(
                "unfound_elements/missing_elements.csv",
                attribute_name,
                attribute_value,
                "Not found in 5s"
            )
        return None

def safe_click(driver, by, value, timeout=10):
    """Scrolls into view, waits until clickable, tries normal + JS click."""
    try:
        elem = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        elem.click()
        return True
    except Exception as e1:
        try:
            driver.execute_script("arguments[0].click();", elem)
            logging.warning(f"Fallback JS click used for {value}")
            return True
        except Exception as e2:
            logging.error(f"❌ safe_click failed for {value}: {e2}")
            return False
# ----------------------------------

def safe_click(driver, by, value, timeout=10):
    """Scrolls into view, waits until clickable, tries normal + JS click."""
    try:
        elem = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        elem.click()
        return True
    except Exception as e1:
        try:
            driver.execute_script("arguments[0].click();", elem)
            logging.warning(f"Fallback JS click used for {value}")
            return True
        except Exception as e2:
            logging.error(f"❌ safe_click failed for {value}: {e2}")
            return False
# ----------------------------------

def safe_click(driver, by, value, timeout=10):
    """Scrolls into view, waits until clickable, tries normal + JS click."""
    try:
        elem = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        elem.click()
        return True
    except Exception as e1:
        try:
            driver.execute_script("arguments[0].click();", elem)
            logging.warning(f"Fallback JS click used for {value}")
            return True
        except Exception as e2:
            logging.error(f"❌ safe_click failed for {value}: {e2}")
            return False
# ----------------------------------

        


def measure_widget_load_time(driver, widget_locator, max_allowed_time=2, timeout=30):
    """
    Waits for widget to load and fails if load time exceeds max_allowed_time (seconds)
    """
    start_time = time.perf_counter()

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(widget_locator)
    )

    end_time = time.perf_counter()
    load_time = round(end_time - start_time, 2)

    logging.info(f"🕒 Widget load time: {load_time} seconds")

    if load_time > max_allowed_time:
        raise AssertionError(
            f"❌ Widget load time {load_time}s exceeded limit of {max_allowed_time}s"
        )

    return load_time

def fill_signup_otp(driver, otp: str):
    otp = str(otp).zfill(6)
    wait = WebDriverWait(driver, 15)

    for i, digit in enumerate(otp):
        otp_field = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"[data-testing-id='otpInput_Register_{i}']")
            )
        )
        otp_field.clear()
        otp_field.send_keys(digit)
        time.sleep(0.2)  # React OTP stability


def get_widget_load_times(driver):
    """
    Capture response times for all widgets after login
    """
    import time
    time.sleep(5)  # extra wait in case widgets are still loading

    logs = driver.get_log("performance")
    request_start_times = {}
    widget_results = []

    for entry in logs:
        log = json.loads(entry["message"])["message"]
        method = log.get("method")

        # 🔹 Capture request start
        if method == "Network.requestWillBeSent":
            request_id = log["params"]["requestId"]
            url = log["params"]["request"]["url"]

            if "/traderboard-nestjs/proxy" in url:  # ✅ filter only widget proxy APIs
                request_start_times[request_id] = {
                    "url": url,
                    "start_time": log["params"]["timestamp"]
                }

        # 🔹 Capture request end
        if method == "Network.loadingFinished":
            request_id = log["params"]["requestId"]

            if request_id in request_start_times:
                end_time = log["params"]["timestamp"]
                start_time = request_start_times[request_id]["start_time"]

                duration_ms = (end_time - start_time) * 1000

                widget_results.append({
                    "url": request_start_times[request_id]["url"],
                    "response_time_ms": round(duration_ms, 2)
                })

                del request_start_times[request_id]

    return widget_results