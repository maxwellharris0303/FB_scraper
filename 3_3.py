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
output_file = 'output_3_3.csv'

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
    profile_with_comment_links = []
    profiles = get_profiles()
    print(len(profiles))

    for profile in profiles:
        profile_link = profile.find_element(By.TAG_NAME, "a")
        link = driver.execute_script("return arguments[0].getAttribute('href');", profile_link)
        link = remove_comment_id_parameter(link)
        profile_with_comment_links.append(link)
    print(profile_with_comment_links)

    def get_post_link(post):
        post_link_parent = post.find_element(By.CSS_SELECTOR, "div[class=\"html-div xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6\"]")
        post_link_a = post_link_parent.find_element(By.TAG_NAME, "a")
        post_link = driver.execute_script("return arguments[0].getAttribute('href');", post_link_a)
        post_link = remove_cft_parameter(post_link)
        if len(post_link) < 30:
            return "NA"
        if not "facebook.com" in post_link:
            post_link = "https://facebook.com" + post_link
        if "comment_id" in post_link:
            return "NA"
        
        return post_link

    for profile_link in profile_with_comment_links:
        driver.get(profile_link)
        sleep(3)
        name = ""
        try:
            h1_elements = driver.find_elements(By.CSS_SELECTOR, "h1[class=\"html-h1 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1vvkbs x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz\"]")
            name = h1_elements[len(h1_elements) - 1].text
            name = name.replace('\u00a0', '')
        except:
            name = "None"
        print(name)
        
        def get_posts():
            while True:
                try:
                    posts = driver.find_elements(By.CSS_SELECTOR, "div[class=\"x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z\"]")
                    break
                except:
                    sleep(0.5)
                    pass
            return posts

        old_count = 0
        new_count = len(get_posts())
        if new_count == 0:
            public = False
        flag = 0
        while True:
            if flag > 10:
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
                pass
            # Wait for new content to load
            sleep(0.5)
            new_count = len(get_posts())
            #######################################
            if new_count > 3:
                break

        able_to_comment = False
        post_link = "NA"
        
        posts = driver.find_elements(By.CSS_SELECTOR, "div[class=\"x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z\"]")
        print(len(posts))
        for post in posts:
            try:
                comment_button = post.find_element(By.CSS_SELECTOR, "div[aria-label=\"Komentari\"]")
                post_link = get_post_link(post)
                print(post_link)
                if post_link != "NA":
                    able_to_comment = True
                    break
            except:
                pass
            try:
                comment_button = post.find_element(By.CSS_SELECTOR, "div[aria-label=\"Comments\"]")
                post_link = get_post_link(post)
                print(post_link)
                if post_link != "NA":
                    able_to_comment = True
                    break
            except:
                pass
            try:
                comment_button = post.find_element(By.CSS_SELECTOR, "div[aria-label=\"Beri komentar\"]")
                post_link = get_post_link(post)
                print(post_link)
                if post_link != "NA":
                    able_to_comment = True
                    break
            except:
                pass
            try:
                comment_button = post.find_element(By.CSS_SELECTOR, "div[aria-label=\"Leave a comment\"]")
                post_link = get_post_link(post)
                print(post_link)
                if post_link != "NA":
                    able_to_comment = True
                    break
            except:
                pass
        print(able_to_comment)
        print(post_link)
        data = {
            "name": name,
            "profile_link": profile_link,
            "able_to_comment": able_to_comment,
            "post_link": post_link
        }
        df = pd.DataFrame([data])

        # Append DataFrame to CSV
        df.to_csv(output_file, mode='a', index=False, header=not file_exists)

        # Set file_exists to True after first write
        file_exists = True