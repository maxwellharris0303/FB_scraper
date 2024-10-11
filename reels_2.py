from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
from time import sleep
import re
import pandas as pd
import login_module

driver = login_module.fb_login()

csv_file_name = "output_reels_2.csv"
df = pd.DataFrame(columns=['Link'])

# Save the DataFrame to create the CSV file if it doesn't exist
df.to_csv(csv_file_name, index=False)

def remove_cft_parameter(link):
    return re.sub(r'\__cft__\[0\].*', '', link)

with open('link_reels_2.txt', 'r') as file:
    lines = file.readlines()
    
for line in lines:
    url = line
    driver.get(url)
    sleep(5)

    while True:
        try:
            next_card_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label=\"Kartu Berikutnya\"]")
            next_card_button.click()
            url = driver.current_url
            print(url)
            with open("output_reels.txt", "a") as file:
                file.write(url + "\n")
        except:
            try:
                next_card_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label=\"Next Card\"]")
                next_card_button.click()
                url = driver.current_url
                print(url)
                # Create a DataFrame for the current link
                df = pd.DataFrame([[url]], columns=['Link'])
                
                # Append the link to the CSV file
                df.to_csv(csv_file_name, mode='a', header=False, index=False)
            except:
                break
            
        sleep(0.3)
