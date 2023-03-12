import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import pandas as pd
#%% set driver options and read URLs data

opts = webdriver.ChromeOptions()

opts.add_argument("start-maximized")

href_df = pd.read_csv(r"F:\Università\goethe\sem3\data\case\scrape\href_df.csv")
#%% open driver and get root URL

driver = webdriver.Chrome(service = Service(r"F:\Università\goethe\sem3\data\chromedriver.exe"),
                          options = opts)

driver.get("https://www.gofundme.com/discover/environment-fundraiser")
#%% click on accept cookies button

driver.find_element(by = By.ID, value = "onetrust-accept-btn-handler").click()
#%% click on change language flag icon

driver.find_element(by = By.CSS_SELECTOR,
                    value = ".footer-locale-picker-flag.norma-icon.norma-icon--circle.mr").click()
#%% select english from drop down menu within change language page; this automatically sets
# country to US, so no additional selection is needed to change the country, even if initially it's
# set to Germany

Select(driver.find_element(by = By.ID,
                           value = "localePickerLanguage")).select_by_value("en")
#%% click on save changes button

driver.find_element(by = By.CSS_SELECTOR,
                    value = ".js-locale-picker-save.button.primary.text-bold").click()
#%% get campaign's URL from csv data

driver.get(href_df["0"][2])

#%% click on read more button if available

try:
    driver.find_element(by = By.CSS_SELECTOR, value = ".hrt-text-button.hrt-text-button--gray-dark").click()
    time.sleep(2)
except:
    pass
#%% scroll to page bottom

window_size = driver.get_window_size()["height"]
window_size = int(window_size / 4)
time.sleep(2)

page_height = driver.execute_script("return document.body.scrollHeight")
time.sleep(2)

for i in range(round(page_height/window_size) + 1):
    driver.execute_script("window.scrollBy(0," + str(window_size) + ");")
    time.sleep(.5)
#%% click on show more button to expose 10 additional comments (1 as 10 comments shown already, loading 10 per time yields 20 comments,
# so covers all 19 available at the time of script execution)

driver.find_element(by = By.XPATH,
                    value = "//button[@class='mt3x hrt-secondary-button hrt-secondary-button--green hrt-secondary-button--full-for-small hrt-secondary-button--medium hrt-base-button']").click()
time.sleep(2)
#%% extract words of support donation amounts

supp_elems = driver.find_elements(by = By.XPATH,
                                  value = "//div[@class='m-donation-and-time']")

supp_don_lst = []
for elem in supp_elems:
    supp_don_lst.append(int(re.findall("\d+", elem.text)[0]))
#%% click on see all button and scroll to donation list bottom

driver.find_element(by = By.CSS_SELECTOR,
                         value = ".mt2x.hrt-secondary-button.hrt-secondary-button--green.hrt-secondary-button--inline.hrt-secondary-button--small.hrt-base-button").click()
time.sleep(2)

#%% scroll to donation list bottom

scrollable_popup = driver.find_element(By.XPATH, value = "//div[@class='o-modal-donations-content']")
for i in range(10):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_popup)
    time.sleep(.5)
#%% extract donation amounts from donation list elements

don_elems = driver.find_elements(by = By.XPATH, value = "//ul[@class='m-donation-meta list-unstyled m-meta-list m-meta-list--bullet']")

don_lst = []
for elem in don_elems:
    don_lst.append(elem.text.partition("\n")[0])
#%% remove duplicates and blank entries from previous list

don_lst = [i for i in don_lst if i]

don_lst = don_lst[0:196]
#%% turn the list into an integer list after replacing characters which prevent it

for w in range(len(don_lst)):
    don_lst[w] = int(don_lst[w].replace("$", "").replace(",", "").replace(" ", ""))
#%% check which and how many values to remove from main list for comparison

supp_don_dct_keys = []

for val in supp_don_lst:
    if val not in supp_don_dct_keys:
        supp_don_dct_keys.append(val)

supp_don_dct_values = []

for val in supp_don_dct_keys:
    counter = 0
    
    for i in range(len(supp_don_lst)):
        if supp_don_lst[i] == val:
            counter += 1
    supp_don_dct_values.append(counter)

supp_don_dct = {supp_don_dct_keys[i]: supp_don_dct_values[i] for i in range(len(supp_don_dct_keys))}
#%% define helper function to remove values exact amount of times

def rem_n_vals(lst, dizio):
    for val in dizio.keys():
        for i in range(dizio[val]):
            lst.remove(val)
    
    return lst
#%% remove donations linked to words of support from main list for average comparison

don_lst_rem = don_lst.copy()

don_lst_rem = rem_n_vals(don_lst_rem, supp_don_dct)
#%% compare averages to show which one is larger

print(pd.Series(don_lst_rem).mean())
print(pd.Series(supp_don_lst).mean())
#%% close driver

driver.close()
