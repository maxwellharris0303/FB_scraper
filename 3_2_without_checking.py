from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
from time import sleep
import re
import pandas as pd
import os
import login_module

USERNAME = "61556074829411"
PASSWORD = "akunfb.id"

# Output CSV file
output_file = 'output_3_2_without_checking.csv'

# Check if the file already exists
file_exists = os.path.isfile(output_file)

driver = login_module.fb_login()

data = {}

def remove_cft_parameter(link):
    return re.sub(r'\__cft__\[0\].*', '', link)

with open('links_to_scrape_3_2.txt', 'r') as file:
    lines = file.readlines()
    
for line in lines:
    url = line

    driver.get(url)
    sleep(5)
    try:
        likers_button = driver.find_element(By.CSS_SELECTOR, "span[class=\"xt0b8zv x2bj2ny xrbpyxo xl423tq\"]")
        likers_button.click()
    except:
        sleep(3)
        likers_button = driver.find_element(By.CSS_SELECTOR, "span[class=\"xt0b8zv x2bj2ny xrbpyxo xl423tq\"]")
        likers_button.click()
        pass
    sleep(1)
    old_count = 0
    try:
        dialog = driver.find_element(By.CSS_SELECTOR, "div[class=\"x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x78zum5 xdt5ytf x1iyjqo2 x1al4vs7\"]")
    except:
        likers_button = driver.find_element(By.CSS_SELECTOR, "span[class=\"xt0b8zv x2bj2ny xrbpyxo xl423tq\"]")
        likers_button.click()
        sleep(1)
        dialog = driver.find_element(By.CSS_SELECTOR, "div[class=\"x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x78zum5 xdt5ytf x1iyjqo2 x1al4vs7\"]")
        pass
    likers = dialog.find_elements(By.CSS_SELECTOR, "div[class=\"xu06os2 x1ok221b\"]")

    old_count = 0
    new_count = len(likers)
    flag = 0
    while True:
        if flag > 10:
            break
        if new_count == old_count:
            flag += 1
        if new_count > old_count:
            old_count = new_count
            flag = 0
        likers_link = []
        dialog = driver.find_element(By.CSS_SELECTOR, "div[class=\"x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x78zum5 xdt5ytf x1iyjqo2 x1al4vs7\"]")
        likers = dialog.find_elements(By.CSS_SELECTOR, "div[class=\"xu06os2 x1ok221b\"]")
        new_count = len(likers)
        print(f"likers-----{new_count}")
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", likers[len(likers) - 1])
        except:
            pass
        sleep(0.2)
    
    names = []
    likers_link = []
    dialog = driver.find_element(By.CSS_SELECTOR, "div[class=\"x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x78zum5 xdt5ytf x1iyjqo2 x1al4vs7\"]")
    likers = dialog.find_elements(By.CSS_SELECTOR, "div[class=\"xu06os2 x1ok221b\"]")
    for liker in likers:
        liker_link_parent = liker.find_element(By.TAG_NAME, "a")
        profile_name = liker_link_parent.text
        profile_name = profile_name.replace('\u00a0', '')
        print(profile_name)
        names.append(profile_name)
        liker_link = driver.execute_script("return arguments[0].getAttribute('href');", liker_link_parent)
        liker_link = remove_cft_parameter(liker_link)
        likers_link.append(liker_link)
    print(likers_link)
    
    for index in range(len(likers_link)):
        data = {
            "name": names[index],
            "profile_link": likers_link[index],
        }
        df = pd.DataFrame([data])

        # Append DataFrame to CSV
        df.to_csv(output_file, mode='a', index=False, header=not file_exists)

        # Set file_exists to True after first write
        file_exists = True