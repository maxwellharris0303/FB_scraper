from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
from time import sleep

USERNAME = "61556074829411"
PASSWORD = "akunfb.id"

def fb_login():
    url = "https://www.facebook.com"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1  # 1: Allow, 2: Block
    })

    # Initialize the WebDriver
    driver = webdriver.Chrome(max_ws_size=2**50, options=chrome_options)

    # driver.maximize_window()
    driver.get(url)
    sleep(3)
    try:
        allow_cookie_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label=\"Allow all cookies\"]")
        allow_cookie_button.click()
        sleep(3)
    except:
        pass

    username_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"email\"]")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"pass\"]")
    username_input.write(USERNAME)
    password_input.write(PASSWORD)

    login_button = driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]")
    login_button.click()
    sleep(10)
    return driver