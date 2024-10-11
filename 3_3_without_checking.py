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
output_file = 'output_3_3_without_checking.csv'

# Check if the file already exists
file_exists = os.path.isfile(output_file)

driver = login_module.fb_login()

data = {}

def remove_cft_parameter(link):
    return re.sub(r'\__cft__\[0\].*', '', link)
def remove_comment_id_parameter(link):
    return re.sub(r'comment_id=.*$', '', link)

with open('links_to_scrape_3_3.txt', 'r') as file:
    lines = file.readlines()
    
for line in lines:
    url = line

    driver.get(url)
    sleep(5)

    spans = driver.find_elements(By.TAG_NAME, "span")
    for span in spans:
        if "Most relevant" in span.text or "Paling relevan" in span.text:
            driver.execute_script("arguments[0].scrollIntoView(false);", span)
            span.click()
            break
    sleep(2)
    spans = driver.find_elements(By.CSS_SELECTOR, "span[class=\"x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h\"]")
    for span in spans:
        if "All comments" in span.text or "Semua komentar" in span.text:
            span.click()
            break
    sleep(5)

    def get_profiles():
        profiles = driver.find_elements(By.CSS_SELECTOR, "div[class=\"x169t7cy x19f6ikt\"]")
        while True:
            try:
                profiles = driver.find_elements(By.CSS_SELECTOR, "div[class=\"x169t7cy x19f6ikt\"]")
                break
            except:
                sleep(0.5)
                pass
        return profiles

    old_count = 0
    new_count = len(get_profiles())
    flag = 0
    while True:
        if flag > 4:
            break
        if new_count == old_count:
            flag += 1
        if new_count > old_count:
            old_count = new_count
            flag = 0
        try:
        # Scroll down by 1000 pixels
            view_more_comments_button = driver.find_element(By.CSS_SELECTOR, "div[class=\"html-div xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x78zum5 x13a6bvl\"]")
            driver.execute_script("arguments[0].scrollIntoView(true);", view_more_comments_button)
            view_more_comments_button.click()
        except:
            break
        # Wait for new content to load
        sleep(3)
        new_count = len(get_profiles())
        print(new_count)
        #######################################
        # if new_count > 30:
        #     break
        
    names = []
    profile_with_comment_links = []
    profiles = get_profiles()
    print(len(profiles))

    for profile in profiles:
        profile_link = profile.find_elements(By.TAG_NAME, "a")
        profile_name = profile_link[1].text
        profile_name = profile_name.replace('\u00a0', '')
        print(profile_name)
        names.append(profile_name)
        link = driver.execute_script("return arguments[0].getAttribute('href');", profile_link[0])
        link = remove_comment_id_parameter(link)
        profile_with_comment_links.append(link)
    print(profile_with_comment_links)

    for index in range(len(profile_with_comment_links)):
        data = {
            "name": names[index],
            "profile_link": profile_with_comment_links[index],
        }
        df = pd.DataFrame([data])

        # Append DataFrame to CSV
        df.to_csv(output_file, mode='a', index=False, header=not file_exists)

        # Set file_exists to True after first write
        file_exists = True