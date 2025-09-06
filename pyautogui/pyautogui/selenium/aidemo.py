#!/usr/bin/env python3
"""
Selenium test script that runs 5 feature tests against https://the-internet.herokuapp.com/
Features:
  1. Add/Remove Elements
  2. Form Authentication (invalid + valid)
  3. Dropdown
  4. JavaScript Alerts (confirm)
  5. Dynamic Controls (remove/add checkbox, enable input)

Uses webdriver-manager to auto install ChromeDriver.
"""

import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

# Configuration
BASE_URL = "https://the-internet.herokuapp.com/"
SCREENSHOT_DIR = "screenshots"
WAIT_TIMEOUT = 10  # seconds

# Make screenshots dir
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def start_driver(headless=False):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.maximize_window()
    return driver


def screenshot(driver, name):
    ts = int(time.time())
    path = os.path.join(SCREENSHOT_DIR, f"{name}_{ts}.png")
    try:
        driver.save_screenshot(path)
    except WebDriverException:
        pass
    return path


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


def safe_find(driver, by, value, timeout=WAIT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


def test_add_remove_elements(driver):
    test_name = "add_remove_elements"
    log(f"START: {test_name}")
    try:
        driver.get(BASE_URL)
        link = safe_find(driver, By.LINK_TEXT, "Add/Remove Elements")
        link.click()

        # Wait for Add Element button
        add_btn = safe_find(driver, By.CSS_SELECTOR, "button[onclick='addElement()']")
        add_btn.click()

        # Now one delete button should appear
        delete_btn = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button.added-manually"))
        )
        assert delete_btn.is_displayed(), "Delete button not visible after adding"

        # Click delete and ensure it's removed
        delete_btn.click()
        # Wait for invisibility or NoSuchElement
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "button.added-manually"))
        )

        log(f"PASS: {test_name}")
        return True
    except Exception as e:
        path = screenshot(driver, test_name)
        log(f"FAIL: {test_name} - {e}\nScreenshot: {path}")
        traceback.print_exc()
        return False


def test_form_authentication(driver):
    test_name = "form_authentication"
    log(f"START: {test_name}")
    try:
        driver.get(BASE_URL)
        link = safe_find(driver, By.LINK_TEXT, "Form Authentication")
        link.click()

        # Invalid login first
        username = safe_find(driver, By.ID, "username")
        password = safe_find(driver, By.ID, "password")
        login_btn = safe_find(driver, By.CSS_SELECTOR, "button[type='submit']")

        username.clear()
        password.clear()
        username.send_keys("wrong_user")
        password.send_keys("wrong_pass")
        login_btn.click()

        # Wait for flash error
        flash = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        assert "Your username is invalid!" in flash.text or "invalid" in flash.text.lower(), \
            f"Expected invalid login message, got: {flash.text}"

        # Now valid login (these credentials are known for this site)
        username = safe_find(driver, By.ID, "username")
        password = safe_find(driver, By.ID, "password")
        username.clear()
        password.clear()
        username.send_keys("tomsmith")
        password.send_keys("SuperSecretPassword!")
        login_btn = safe_find(driver, By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()

        # Wait for success flash and secure area
        flash = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        assert "You logged into a secure area!" in flash.text or "logged into a secure" in flash.text.lower()

        # Logout to leave the app in known state
        logout_btn = safe_find(driver, By.LINK_TEXT, "Logout")
        logout_btn.click()

        log(f"PASS: {test_name}")
        return True
    except Exception as e:
        path = screenshot(driver, test_name)
        log(f"FAIL: {test_name} - {e}\nScreenshot: {path}")
        traceback.print_exc()
        return False


def test_dropdown(driver):
    test_name = "dropdown"
    log(f"START: {test_name}")
    try:
        driver.get(BASE_URL)
        link = safe_find(driver, By.LINK_TEXT, "Dropdown")
        link.click()

        select_el = safe_find(driver, By.ID, "dropdown")
        sel = Select(select_el)

        # Select Option 2 and verify
        sel.select_by_visible_text("Option 2")
        selected = sel.first_selected_option
        assert selected.text.strip() == "Option 2", f"Expected Option 2, got {selected.text}"

        # Select Option 1 and verify
        sel.select_by_visible_text("Option 1")
        selected = sel.first_selected_option
        assert selected.text.strip() == "Option 1", f"Expected Option 1, got {selected.text}"

        log(f"PASS: {test_name}")
        return True
    except Exception as e:
        path = screenshot(driver, test_name)
        log(f"FAIL: {test_name} - {e}\nScreenshot: {path}")
        traceback.print_exc()
        return False


def test_javascript_alerts(driver):
    test_name = "javascript_alerts"
    log(f"START: {test_name}")
    try:
        driver.get(BASE_URL)
        link = safe_find(driver, By.LINK_TEXT, "JavaScript Alerts")
        link.click()

        # Click JS Confirm
        btn_confirm = safe_find(driver, By.XPATH, "//button[text()='Click for JS Confirm']")
        btn_confirm.click()

        # Wait for alert and accept
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.alert_is_present())
        alert = Alert(driver)
        alert_text = alert.text
        assert "confirm" in alert_text.lower() or len(alert_text) > 0
        alert.accept()

        # Verify result text
        result = safe_find(driver, By.ID, "result")
        assert "You clicked: Ok" in result.text or "You clicked: Ok".lower() in result.text.lower() or "ok" in result.text.lower()

        log(f"PASS: {test_name}")
        return True
    except Exception as e:
        path = screenshot(driver, test_name)
        log(f"FAIL: {test_name} - {e}\nScreenshot: {path}")
        traceback.print_exc()
        return False


def test_dynamic_controls(driver):
    test_name = "dynamic_controls"
    log(f"START: {test_name}")
    try:
        driver.get(BASE_URL)
        link = safe_find(driver, By.LINK_TEXT, "Dynamic Controls")
        link.click()

        # Remove checkbox
        chk_selector = (By.CSS_SELECTOR, "#checkbox")
        btn_remove = safe_find(driver, By.CSS_SELECTOR, "#checkbox-example button")
        btn_remove_text = btn_remove.text.strip().lower()
        btn_remove.click()

        # Wait until checkbox absent
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.invisibility_of_element_located(chk_selector))

        # Click Add (same button switches to Add)
        btn_add = safe_find(driver, By.CSS_SELECTOR, "#checkbox-example button")
        btn_add.click()
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located(chk_selector))

        # Now test enabling input
        enable_btn = safe_find(driver, By.CSS_SELECTOR, "#input-example button")
        enable_btn.click()
        # Wait until input is enabled
        input_el = safe_find(driver, By.CSS_SELECTOR, "#input-example input")
        WebDriverWait(driver, WAIT_TIMEOUT).until(lambda d: input_el.is_enabled())
        # Type into enabled input
        input_el.clear()
        input_el.send_keys("Selenium test")
        assert input_el.get_attribute("value") == "Selenium test"

        # Disable input again to reset
        disable_btn = safe_find(driver, By.CSS_SELECTOR, "#input-example button")
        disable_btn.click()
        WebDriverWait(driver, WAIT_TIMEOUT).until(lambda d: not input_el.is_enabled())

        log(f"PASS: {test_name}")
        return True
    except Exception as e:
        path = screenshot(driver, test_name)
        log(f"FAIL: {test_name} - {e}\nScreenshot: {path}")
        traceback.print_exc()
        return False


def main():
    headless = False  # set True if you want headless mode
    driver = start_driver(headless=headless)
    results = {}
    try:
        results["add_remove_elements"] = test_add_remove_elements(driver)
        results["form_authentication"] = test_form_authentication(driver)
        results["dropdown"] = test_dropdown(driver)
        results["javascript_alerts"] = test_javascript_alerts(driver)
        results["dynamic_controls"] = test_dynamic_controls(driver)
    finally:
        driver.quit()

    log("TEST SUMMARY")
    for k, v in results.items():
        log(f"  {k}: {'PASS' if v else 'FAIL'}")

    # exit code: 0 if all pass, 1 otherwise
    all_pass = all(results.values())
    exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
