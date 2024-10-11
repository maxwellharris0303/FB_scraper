from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
from time import sleep
import re
import pandas as pd
import os
import login_module

LIMIT = 30

# Output CSV file
output_file = 'output_3_1_without_checking.csv'

# Check if the file already exists
file_exists = os.path.isfile(output_file)

driver = login_module.fb_login()

data = {}

def remove_cft_parameter(link):
    return re.sub(r'\__cft__\[0\].*', '', link)

with open('links_to_scrape_3_1.txt', 'r') as file:
    lines = file.readlines()
    
for line in lines:
    profile_url = line

    if "id=" in profile_url:
        profile_url = profile_url + "&sk=friends"
    else:
        profile_url = profile_url + "/friends"

    driver.get(profile_url)
    def get_profiles():
        profiles = driver.find_elements(By.CSS_SELECTOR, "div[class=\"x1iyjqo2 x1pi30zi\"]")
        while True:
            try:
                profiles = driver.find_elements(By.CSS_SELECTOR, "div[class=\"x1iyjqo2 x1pi30zi\"]")
                break
            except:
                sleep(0.5)
                pass
        return profiles

    old_count = 0
    new_count = len(get_profiles())
    flag = 0
    while True:
        if flag > 30:
            break
        if new_count == old_count:
            flag += 1
        if new_count > old_count:
            old_count = new_count
            flag = 0
        try:
        # Scroll down by 1000 pixels
            driver.execute_script("window.scrollBy(0, 1000);")
        except:
            break
        # Wait for new content to load
        sleep(0.2)
        new_count = len(get_profiles())
        print(new_count)
        #######################################
        if new_count > LIMIT:
            break

    names = []
    friends_links = []
    profiles = get_profiles()
    print(len(profiles))
    for profile in profiles:
        profile_link = profile.find_element(By.TAG_NAME, "a")
        profile_name = profile_link.text
        profile_name = profile_name.replace('\u00a0', '')
        print(profile_name)
        names.append(profile_name)
        link = driver.execute_script("return arguments[0].getAttribute('href');", profile_link)
        link = remove_cft_parameter(link)
        friends_links.append(link)
    print(friends_links)
    
    for index in range(len(friends_links)):
        data = {
            "name": names[index],
            "profile_link": friends_links[index],
        }
        df = pd.DataFrame([data])

        # Append DataFrame to CSV
        df.to_csv(output_file, mode='a', index=False, header=not file_exists)

        # Set file_exists to True after first write
        file_exists = True