from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
from time import sleep
import re
import pandas as pd
import login_module

search_word = "fence"

driver = login_module.fb_login()

csv_file_name = "output_public_post.csv"
df = pd.DataFrame(columns=['Link'])

# Save the DataFrame to create the CSV file if it doesn't exist
df.to_csv(csv_file_name, index=False)

def remove_cft_parameter(link):
    return re.sub(r'\__cft__\[0\].*', '', link)

url = f"https://www.facebook.com/search/posts?q={search_word}&filters=eyJycF9hdXRob3I6MCI6IntcIm5hbWVcIjpcIm1lcmdlZF9wdWJsaWNfcG9zdHNcIixcImFyZ3NcIjpcIlwifSJ9"
driver.get(url)
sleep(5)

def get_feeds():
    search_result = driver.find_element(By.CSS_SELECTOR, "div[class=\"x193iq5w x1xwk8fm\"]")
    div_elements = search_result.find_elements(By.XPATH, './div')
    while True:
        try:
            search_result = driver.find_element(By.CSS_SELECTOR, "div[class=\"x193iq5w x1xwk8fm\"]")
            div_elements = search_result.find_elements(By.XPATH, './div')
            break
        except:
            sleep(0.5)
            pass
    return div_elements

old_count = 0
new_count = len(get_feeds())
flag = 0
while True:
    if flag > 30:
        break
    if new_count == old_count:
        flag += 1
    if new_count > old_count:
        old_count = new_count
        flag = 0
        
        search_result = driver.find_element(By.CSS_SELECTOR, "div[class=\"x193iq5w x1xwk8fm\"]")
        a_links = search_result.find_elements(By.TAG_NAME, "a")
        print(len(a_links))
        for a_link in a_links:
            link = driver.execute_script("return arguments[0].getAttribute('href');", a_link)
            link = remove_cft_parameter(link)
            if not "facebook.com" in link:
                link = "https://facebook.com" + link
            if "hashtag" not in link and any(sub in link for sub in ["reel", "videos", "photo"]):
                print(link)
                
                # Create a DataFrame for the current link
                df = pd.DataFrame([[link]], columns=['Link'])
                
                # Append the link to the CSV file
                df.to_csv(csv_file_name, mode='a', header=False, index=False)
    try:
    # Scroll down by 1000 pixels
        driver.execute_script("window.scrollBy(0, 1000);")
    except:
        break
    # Wait for new content to load
    sleep(0.2)
    new_count = len(get_feeds())
    print(new_count)
    #######################################