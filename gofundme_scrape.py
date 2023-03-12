import time
import re

from selenium import webdriver
#from selenium.webdriver.chrome.options import Options thought it was needed for following cell
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.common.keys import Keys

import numpy as np
import pandas as pd

import datetime as dt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
#%% set browser to open maximized, tried to add it directly as chrome_options below, but didn't work;
# also added the argument "disable-notifications" thinking it would prevent cookie popup, but didn't

opts = webdriver.ChromeOptions()

opts.add_argument("start-maximized")
#%% set driver path and open root URL

driver = webdriver.Chrome(service = Service(r"chromedriver.exe"),
                          options = opts)

driver.get("https://www.gofundme.com/discover/environment-fundraiser")
#%% print html code for root page, used it to double check for names, since initially i opened
# inspect page through website which was already in english, but driver opened it in italian,
# so it could lead to not recognizing the names i would input

#print(driver.page_source)
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
#%% define a function returning the date as a datetime object, to use for campaigns created less than 1 week ago, taken and adapted
# from https://stackoverflow.com/questions/28268818/how-to-find-the-date-n-days-ago-in-python

def get_past_date(str_days_ago):
    TODAY = dt.date.today()
    splitted = str_days_ago.split()
    if len(splitted) == 1 and splitted[0].lower() == 'today':
        return str(TODAY.isoformat())
    elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
        date = TODAY - relativedelta(days=1)
        return str(date.isoformat())
    elif splitted[1].lower() in ['hour', 'hours', 'hr', 'hrs', 'h']:
        date = dt.datetime.now() - relativedelta(hours=int(splitted[0]))
        return str(date.date().isoformat())
    elif splitted[1].lower() in ['day', 'days', 'd']:
        date = TODAY - relativedelta(days=int(splitted[0]))
        return str(date.isoformat())
    else:
        return "Wrong Argument format"
#%% extract creation information and remove the distracting substring to isolate date information

#creation = driver.find_element(by = By.CSS_SELECTOR,
 #                              value = ".m-campaign-byline-created.a-created-date.show-for-large").text

#creation = creation.replace("Created ", "")
#%% use the function defined above for recent campaigns

#prova1 = get_past_date(creation)

#prova1 = datetime.strptime(prova1, "%Y-%m-%d").date()
#%% use datetime to directly obtain the date for older campaigns

#date = datetime.strptime(creation, '%B %d, %Y').date()
#%% create date list for creation column
#date_lst = []

#for lnk in href_df["0"]:
 #   driver.get(lnk)
  #  time.sleep(5)
    
   # creation = driver.find_element(by = By.CSS_SELECTOR,
   #                                value = ".m-campaign-byline-created.a-created-date.show-for-large").text

#    creation = creation.replace("Created ", "")

 #   try:
  #      date = datetime.strptime(creation, "%B %d, %Y").date()
    #except:
     #   date = get_past_date(creation)
      #  date = datetime.strptime(date, "%Y-%m-%d").date()
    
    #date_lst.append(date)
    #time.sleep(5)
#%% scroll down towards page bottom, repeat for length adapted to individual page

#window_size = driver.get_window_size()["height"]
#window_size = int(window_size / 4)

#page_height = driver.execute_script("return document.body.scrollHeight")


#for i in range(round(page_height/window_size) + 1):
 #   driver.execute_script("window.scrollBy(0," + str(window_size) + ");")
  #  time.sleep(.5)
#%% click on "Show more" button to expose additional campaigns; do this 16 times
# to expose 204 campaigns overall, since initially 12 campaigns are showed, and pressing
# on the button 16 times exposes 192 more, totalling 204; this is because the task requires
# to gather information about 200 campaigns

for i in range(16):
    driver.find_element(by = By.CSS_SELECTOR,
                        value = ".button.hollow.expanded-mobile.js-load-more-results").click()
    time.sleep(2)
#%% access campaign's URL

#driver.find_element(by = By.CSS_SELECTOR, value = ".hrt-text-button.hrt-text-button--gray-dark").click()

#%% extract campaign's title

#title = driver.find_element(by = By.CSS_SELECTOR, value = ".mb0.p-campaign-title").text
#%% if exists, click read more button within description, else just extract description;
# potential problem since the selector isn't really uniquely identifying the button,
# with name such as "description-read-more-btn", but simply identifies the button as a text button
# which is dark grey, so it may be the case that in other pages another button identified like this one
# exists, but doesn't return "read more", but another action? best way i guess is to try for all
# the needed campaigns and see what happens UPDATE: works for the chosen 204 campaigns

#try:
 #   driver.find_element(by = By.CSS_SELECTOR, value = ".hrt-text-button.hrt-text-button--gray-dark").click()
  #  desc = driver.find_element(by = By.CSS_SELECTOR, value = ".o-campaign-description").text.replace("\n", "")
#except:
 #   desc = driver.find_element(by = By.CSS_SELECTOR, value = ".o-campaign-description").text.replace("\n", "")
#%% extract campaign's organizer; probably not going to work well since it's tailored for the
# specific organizer's name (what if organization instead of firstname + lastname? what if
# organizer didn't register with capital letters? may have been abreanna garcia? maybe
# better to write regex to isolate words before "is organizing"?); also probably not the best
# element to use to extract organizer, since below this field there's a field called "Organizer",
# containing only the name, without "is organizing..", will try to extract from there

#organ_lst = re.findall(r"\b[A-Z][a-z]+\b",
#                       driver.find_element(by = By.CSS_SELECTOR,
#                                           value = ".m-campaign-byline-description").text)

#organ = " ".join(organ_lst)
#%% extract campaign's organizer UPDATE using .m-person-info-name as css selector returns "anonymous",
# works with xpath; PROBLEM doesn't work for other page since the xpath is specific for the browsed one,
# but same information may be contained in different xpath in another page, as it is the case for [1]

#organ = driver.find_element(by = By.XPATH, value = "//*[@id='campaign-members']/div/div[1]/div/div[2]/div[1]").text
#%% extract organizer for [1] without xpath, works for this one but not for [0] as organizer's
# information is contained within .m-person-info-name there, and in that case it leads to "anonymous",
# and not to the actual name

#organ = driver.find_element(by = By.CSS_SELECTOR, value = ".m-organization-info-content-child").text
#%% find location within "learn more" window for charity; can use existence of learn more button
# as condition to state that organizer is a charity? in this case xpath may be same regardless of
# campaign, try and except again?

#print(driver.find_element(by = By.XPATH, value = "//*[@id='portal']/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]").text)
#%% extract campaign's location, copied the xpath with right click on the element within inspect,
# since i tried to use css_selector but got another result, and then tried to write the xpath
# myself, namely //div[@class='m-person-info-content'/div[@class='text-small'], but got an error;
# i think css selector didn't work because this element is nested into the organizer's content element
# UPDATE also this doesn't work for [1], since it's tied to xpath which is unique for the page being
# browsed

#locat = driver.find_element(by = By.XPATH,
#                            value = "//*[@id='campaign-members']/div/div[1]/div/div[2]/div[2]/div[2]").text
#%% save the exposed campaigns using image selector

camp_elems = driver.find_elements(by = By.CSS_SELECTOR,
                                  value = ".cell.grid-item.small-6.medium-4.js-fund-tile [href]")
#%% extract urls leading to campaigns from campaign list

href_lst = []

for i in range(len(camp_elems)):
    href_lst.append(camp_elems[i].get_attribute("href"))
#%% write href list to csv to save time for further trials

#href_df = pd.DataFrame(href_lst)

#href_df.to_csv(r"href_df.csv", index = False)

#href_df = pd.read_csv(r"href_df.csv")
#%% extract info for 204 campaigns, and store it into lists to be transformed into dataframe columns later on
# use less nested css selectors to identify information about organizer;
# interesting to note that the second partition element is an empty string in both [0] and [1] cases;
# this may be helpful to identify first partition element as organizer's name, and third element
# as type of organization/individual and location, without having to use xpath which fails when
# applied to other pages; UPDATE for charity page, must click on the learn more button,
# and use more nested partition to extract location, and then click on the cross to close the learn more
# page

date_lst = []
title_lst = []
desc_lst = []
organ_lst = []
ent_lst = []
loc_lst = []
benef_lst = []
goal_lst = []
raised_lst = []
donations_lst = []
words_lst =  []
up_lst = []
up_txt_lst = []

for lnk in href_lst:
    driver.get(lnk)
    time.sleep(2)
    
    creation = driver.find_element(by = By.CSS_SELECTOR,
                                   value = ".m-campaign-byline-created.a-created-date.show-for-large").text

    creation = creation.replace("Created ", "")

    try:
        date = datetime.strptime(creation, "%B %d, %Y").date()
    except:
        date = get_past_date(creation)
        date = datetime.strptime(date, "%Y-%m-%d").date()
    
    date_lst.append(date)
    time.sleep(2)

    title = driver.find_element(by = By.CSS_SELECTOR, value = ".mb0.p-campaign-title").text
    title_lst.append(title)
    time.sleep(2)
    
    try:
        driver.find_element(by = By.CSS_SELECTOR, value = ".hrt-text-button.hrt-text-button--gray-dark").click()
        time.sleep(2)
        desc = driver.find_element(by = By.CSS_SELECTOR, value = ".o-campaign-description").text.replace("\n", "")
    except:
        desc = driver.find_element(by = By.CSS_SELECTOR, value = ".o-campaign-description").text.replace("\n", "")
    
    desc_lst.append(desc)
    time.sleep(2)
    
    try:
        goal = re.findall("\d+,*\d*,*\d*", driver.find_element(by = By.CSS_SELECTOR,
                                                               value = ".m-progress-meter-heading").text)[1]
    except:
        goal = "0"
    
    goal_lst.append(goal)
    time.sleep(2)
    
    try:
        raised = re.findall("\d+,*\d*,*\d*", driver.find_element(by = By.CSS_SELECTOR,
                                                                 value = ".m-progress-meter-heading").text)[0]
    except:
        raised = "0"
    
    raised_lst.append(raised)
    time.sleep(2)
    
    try:
        donations = re.findall("[\d+.]*\d*", driver.find_element(by = By.CSS_SELECTOR,
                                                                 value = ".mb2x.show-for-large.text-stat.text-stat-title").text)[0]
    except:
        donations = "0"
    
    donations_lst.append(donations)
    time.sleep(2)
    
    window_size = driver.get_window_size()["height"]
    window_size = int(window_size / 4)
    time.sleep(2)
    
    page_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(2)
    
    for i in range(round(page_height/window_size) + 1):
        driver.execute_script("window.scrollBy(0," + str(window_size) + ");")
        time.sleep(.5)
    
    try:
        up_txt = driver.find_element(by = By.CSS_SELECTOR, value = ".m-update-content").text
        up = 1
    except:
        up_txt = "No text available"
        up = 0
    
    up_txt_lst.append(up_txt)
    up_lst.append(up)
    time.sleep(2)
    
    try:
        info = driver.find_element(by = By.CSS_SELECTOR, value = ".m-campaign-members-main-organizer").text
        time.sleep(2)
        organ = info.partition("\n")[0]
        ent = info.partition("\n")[2].partition("\n")[0]
        try:
            if "team" in driver.find_element(by = By.CSS_SELECTOR, value = ".m-campaign-members-header-title").text and "Raised" in driver.find_element(by = By.CSS_SELECTOR, value = ".m-campaign-members-main-organizer").text:
                loc = info.partition("\n")[2].partition("\n")[2].partition("\n")[2]
                time.sleep(2)
            else:
                loc = info.partition("\n")[2].partition("\n")[2]
        except:
            loc = info.partition("\n")[2].partition("\n")[2]
    except:
        driver.find_element(by = By.CSS_SELECTOR,
                            value = ".text-small.m-charity-modal-button.hrt-text-button.hrt-text-button--gray-dark").click()
        time.sleep(2)
        info = driver.find_element(by = By.CSS_SELECTOR, value = ".m-organization-info-content").text
        organ = info.partition("\n")[0]
        ent = info.partition("\n")[2].partition("\n")[0]
        loc = info.partition("\n")[2].partition("\n")[2].partition("\n")[0]
        time.sleep(2)
        driver.find_element(by = By.CSS_SELECTOR,
                            value = ".o-modal-close-TertiaryIconButton.hrt-tertiary-icon-button.hrt-tertiary-icon-button--medium.hrt-base-button").click()
    
    organ_lst.append(organ)
    ent_lst.append(ent)
    loc_lst.append(loc)
    time.sleep(2)
    
    try:
        benef = driver.find_element(by = By.CSS_SELECTOR, value = ".m-campaign-members-main-beneficiary").text.partition("\n")[0]
    except:
        benef = "No beneficiary"
    
    benef_lst.append(benef)
    time.sleep(2)
    
    try:
        words_num = re.findall("\d+,*\d*", driver.find_element(by = By.ID, value = "comments").text)[0]
    except:
        words_num = "0"
    
    words_lst.append(words_num)
    
    time.sleep(3)
# on iteration 4 (index 3), got the error "list index out of range" when running goal command; solved after changing regex from
# "\d+,\d+" to "\d+,*\d*", since this now matches also numbers below 1000, which appear on gofundme without comma (reason why i changed
# , to ,* where * matches 0 or more occurrences), and i also changed \d+ to \d* because this probably matches new campaigns having
# collected 0 so far, which wouldn't appear as 0,000

# got a no such element error when trying to extract donations amount on iteration 38, saw the page and formatting was strange,
# with zoomed in text and images, no donations amount information was visible indeed, while all the previous information was
# correctly extracted; trying to go back into previous campaigns yielded error 403, maybe i should add time.sleep, and this
# error occurred because the website blocked me? will anyways try again with same structure, but replacing "\d+" with "\d*" in regex
# for donations to see if that was the problem

# still got same error, but on iteration 42? will try to add try except clause for donations to see how far it goes, and will assume
# that if button can't be found then donations are 0, even if this is most likely wrong, because then raised amount should be 0 too,
# which is not the case, but setting it as something like "donations not found" would imply that the data type for the donations column
# is mixed (integers with strings), potentially causing problems later on

# got the same error for campaign title on iteration 39, my idea is that the website realizes around that iteration that i'm scraping,
# thus blocking my access, and sometimes this doesn't happen immediately before loading the next campaign so that i'm still able to
# extract some info, but then i'll reach one which hasn't been loaded since the website blocked me, thus i'll get this error;
# will try to increase time sleep to see what happens

# got list index out of range when running goal command at iteration 187, not sure why because running regex correctly finds the amount,
# but maybe something went wrong with connection at that point since only extracted field was title, whereas all other fields were empty
# starting from description UPDATE happened again, i don't really get why; eventually worked but yielded missing values for info,
# from which organ, entity and location derive, so i just dropped the row, even if i managed to extract the information correctly with
# the same try except clause, don't get why this specific url https://www.gofundme.com/f/put-more-greenery-back-into-our-ecosystem
# is problematic but i preferred just omitting it, since the number of campaigns is still beyond 200

# donations over 999 don't appear as 1000+ but as 1K+, potentially as 1.xK (ex. 1.4K), so numbers in the df are wrong;
# solution can be to extract number with dot and subsequent digit, to then manipulate the resulting list to turn it into integers after
# multiplying by 100 (ex. 11.4K is entered as 11.4, turned into 114 and multiplied by 100 to obtain 11400)
#%% define a function converting donation lst elements from str into int

def don_int(donat_lst):
    for i in range(len(donat_lst)):
        if "." in donat_lst[i]:
            donat_lst[i] = donat_lst[i].replace(".", "")
            donat_lst[i] = int(donat_lst[i]) * 100
        else:
            donat_lst[i] = int(donat_lst[i])
    return donat_lst
        
donations_lst = don_int(donations_lst)
#%% define a function converting str into int 

def lst_int(lst):
    for i in range(len(lst)):
        lst[i] = lst[i].replace(",", "")
        lst[i] = int(lst[i])
    return lst

goal_lst = lst_int(goal_lst)
raised_lst = lst_int(raised_lst)
words_lst = lst_int(words_lst)
#%% convert entity, update lists into dummies and create dummy list from beneficiary

for k in range(len(ent_lst)):
    if ent_lst[k] == "Organizer":
        ent_lst[k] = 0
    else:
        ent_lst[k] = 1
    
    if up_lst[k] == "No updates":
        up_lst[k] = 0
    else:
        up_lst[k] = 1

ben_dum_lst = []
for j in range(len(benef_lst)):
    if benef_lst[j] == "No beneficiary":
        ben_dum_lst.append(0)
    else:
        ben_dum_lst.append(1)
#%% form dataframe with extracted information

#df2 = pd.DataFrame(data = {"title": title_lst, "description": desc_lst, "organizer": organ_lst, "entity": ent_lst, "location": loc_lst,
 #                         "beneficiary": benef_lst, "goal": goal_lst, "raised": raised_lst, "donations": donations_lst, "support": words_lst,
  #                        "updates": up_lst, "update_text": up_txt_lst})
# final df with info about support and updates to attach as further reference, explaining that somehow after 20 campaigns elements
# related to support and updates fail to load and i haven't found a reason for this
#%%

df = pd.DataFrame(data = {"creation": date_lst, "title": title_lst, "description": desc_lst, "organizer": organ_lst, "location": loc_lst,
                          "beneficiary": benef_lst, "goal": goal_lst, "raised": raised_lst, "donations": donations_lst, "support": words_lst,
                          "benef_dummy": ben_dum_lst, "entity": ent_lst, "updates": up_lst})
# final df without info about support and updates, since it's only available for first 20 companies
#%% check for duplicate rows (conceptually any column could have duplicates individually, and theoretically even title or description
# could have duplicates if the campaign was somehow published multiple times on the website, but raised/donations/words entries
# would likely be different)

print(df.duplicated().sum())

df = df.replace("", np.nan)

print(df[df.isna().any(axis=1)])

df = df.dropna(axis = 0, how = "any").reset_index(drop = True)
# no duplicates found, only row 187 with empty entries which are converted into nans for easy removal; index is finally reset
#%% save df to excel

df.to_excel(r"camp_info.xlsx", index = False)
# mostly the dataframe is ok, but some lines in the "loc" column highlight a problem occurring for campaigns which are carried out
# by a team, namely by more than one individual/company; in these cases, the location query extracts the location (city, state)
# along with strings like "Raised 100 dollars with 20 donations", since the partition apparently doesn't isolate the location,
# but also the string directly above; a solution may be to further partition such entries after having entered them into the dataframe,
# or setting an additional condition within the loc query to use a different partition when dealing with campaigns carried out by teams

# another issue which i observed when browsing the file is that some entries, such as the one related to URL
# https://www.gofundme.com/f/mt-tam-steep-ravine-bridge-repair?qid=8c7e58bb54c29bb9017771b2eec16636, are related to charities,
# as shown by the description which states that donations are fully tax deductible, but since the organizer field doesn't state
# this by including the "registered nonprofit" string, since the campaign is formatted like as if the organizer was an individual,
# then my code doesn't recognize this campaign as being carried out by a charity; a solution may be to identify names containing
# words typically characterizing charities (such as "Friends" in this case), to then label the entity as a charity in the "ent" column

# some campaigns are carried out on behalf of a third party, named beneficiary, my code doesn't highlight such campaigns, which are
# recognized as campaigns carried out by individuals or charities for their own account (they miss info about beneficiary); this is the
# case for the URL:
# https://www.gofundme.com/f/citizens-against-terramor?qid=8c7e58bb54c29bb9017771b2eec16636, which is also an instance of an atypical
# organizer recognized as individual ("citizens against terramor", which may not be a charity but still clearly isn't an individual)

# the url https://www.gofundme.com/f/rickshaw-running-for-cool-earth contains a campaign run by a team, with an organizer and two
# members, on behalf of a charity (registered nonprofit), but my code only extracts information about the main organizer, labelling this
# as an individual campaign

# potentially solved the "raised x dollars through y donations" issue by adding an if clause within a new try and except
# linked to the header of the campaign, to check whether containing the word "team"; in this case the partition is slightly different
# and allows to omit the "raised" part, just keeping the location; had to add else clause to form "loc" variable in campaigns where
# "team" doesn't appear, maybe not the best solution since i still write the same partition in the except clause right after

# "raised" problem was fixed, but now few entries have empty values in "loc" column due to some campaigns not having the
# "raised" string under organizer info, even if being a team campaign; in this case, the standard partition works to retrieve the location;
# added an and clause to check for the presence of "Raised" in the info box, in which case apply the modified partition, else use the normal
# one

# the url https://www.gofundme.com/f/save-green-space-in-central-coventry?qid=5afcc005337ffbb6dbe179d614359159
# didn't return any word of support, even though there is one, and the regex applied individually indeed returned 1, why is this the case?
# could be that time sleep is too less so that page isn't fully loaded before an error returns

# potential issues can be mixed datatype for words number (try with str and except with int)
#%% scroll to element (only works with already loaded elements i guess)

#boh = driver.find_element(by = By.ID, value = "comments").text

#driver.execute_script("arguments[0].scrollIntoView();", boh)
#%% add column to df in the specified index, shifting others to the right

#df.insert(0, "creation", date_lst)
#%% close driver

driver.close()