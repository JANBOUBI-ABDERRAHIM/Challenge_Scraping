import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from helper import *

def scrap(key_words=['maroc', 'morocco', 'المغرب'], start_date="2023-11-12", end_date="2023-12-12", waiting_time=3):
    url = "https://www.tiktok.com/en/"
    RESULTS = {"date": [], "user/page_name": [], "description": [], "media link": [], "tags": []}
    driver = webdriver.Chrome()
    driver.get(url)
    for i in range(len(key_words)):
        if i==0:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'css-1anes8e-StyledIcon')))

        if len(driver.find_elements(By.CLASS_NAME, 'css-1anes8e-StyledIcon')) != 0:
            driver.find_element(By.CLASS_NAME, 'css-1anes8e-StyledIcon').click()

        time.sleep(waiting_time)
        driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/input').click()
        driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/input').send_keys(Keys.CONTROL + "a")
        driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/input').send_keys(Keys.DELETE)
        driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/input').send_keys(key_words[i])
        driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/button').click()
        time.sleep(waiting_time)
        driver.find_element(By.XPATH, '//*[@id="search-tabs"]/div[1]/div[1]/div[1]/div[3]').click()
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, 'css-1soki6-DivItemContainerForSearch')))

        while True:
            initial_length = len(driver.find_elements(By.CLASS_NAME, 'css-1soki6-DivItemContainerForSearch'))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(waiting_time)
            new_length = len(driver.find_elements(By.CLASS_NAME, 'css-1soki6-DivItemContainerForSearch'))
            if new_length==initial_length:
                break
            new_length = initial_length


        DATES = [i.get_attribute('innerText') for i in driver.find_elements(By.CLASS_NAME, 'css-dennn6-DivTimeTag')]
        IDX   = [i for i in range(len(DATES)) if is_date_between(DATES[i], start_date, end_date)]
        [RESULTS["date"].append(transform_date(DATES[i], False)) for i in IDX]

        ITEMS        = driver.find_elements(By.CLASS_NAME, 'css-1soki6-DivItemContainerForSearch')
        MESSAGES     = [item.find_elements(By.CLASS_NAME, 'css-j2a19r-SpanText') for item in ITEMS]
        DESCRIPTIONS = [[desc.get_attribute('innerText') for desc in message] for message in MESSAGES]
        [RESULTS["description"].append(DESCRIPTIONS[i]) for i in IDX]

        USERNAMES = [i.get_attribute('innerText') for i in driver.find_elements(By.CLASS_NAME, 'css-2zn17v-PUniqueId')]
        [RESULTS["user/page_name"].append(USERNAMES[i]) for i in IDX]

        LINKS = [i.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href') for i in driver.find_elements(By.CLASS_NAME, 'css-1as5cen-DivWrapper')]
        [RESULTS["media link"].append(LINKS[i]) for i in IDX]

        ALL_TAGS = [item.find_elements(By.CLASS_NAME, 'ejg0rhn6') for item in ITEMS]
        TAGS     = [[tag.find_elements(By.CLASS_NAME, 'css-1p6dp51-StrongText')[0].get_attribute('innerText') for tag in tag_content] for tag_content in ALL_TAGS]
        [RESULTS["tags"].append(TAGS[i]) for i in IDX]

    save_results(RESULTS)
    # results = pd.DataFrame(RESULTS)
    # results = results.drop_duplicates(subset=['media link'])
    # FILTRED_DESCRIPTIONS = [[description for description in results['description'].iloc[idx] if description not in ['', ' ']] for idx in range(len(results))]
    # results['description'] = FILTRED_DESCRIPTIONS
    # results.to_csv("RESULTS.csv", index=False)


if __name__ == "__main__":
    CLI = argparse.ArgumentParser()
    CLI.add_argument("--keywords",     type=str, default=['maroc', 'morocco', 'المغرب'], nargs="*")
    CLI.add_argument("--start_date",   type=str, default="2023-11-12")
    CLI.add_argument("--end_date",     type=str, default="2023-12-12")
    CLI.add_argument("--waiting_time", type=int, default=3)

    args = CLI.parse_args()
    
    keywords     = args.keywords
    start_date   = args.start_date
    end_date     = args.end_date
    waiting_time = args.waiting_time

    print("keywords:     %r" % type(keywords), keywords)
    print("start_date:   %r" % type(start_date), start_date)
    print("end_date:     %r" % type(end_date), end_date)
    print("waiting_time: %r" % type(waiting_time), waiting_time)

    scrap(keywords, start_date, end_date, waiting_time)

# python SCRAP.py --keywords maroc morocco --start_date 2023-11-12 --end_date 2023-12-12 --waiting_time 3