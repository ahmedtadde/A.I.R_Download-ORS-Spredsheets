
# coding: utf-8

# In[ ]:

import sys
set_variables = raw_input('Did you check and set values for ALL the variables url, username, password, districts_selection_type, and districts_selection in this scripts')

if set_variables.lower() != 'yes':
    print 'It must be done before procceding... otherwise you will download data for the wrong districts!'
    print 'After setting variables to desired values. Re-run the script.'
    sys.exit()

try:
    import selenium
except ImportError:
    print 'the selenium module must be installed by entering one of the following statements:'
    print 'pip install selenium' 
    print '!pip install selenium'
    print 'After installation, re-run script'
    sys.exit()

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import re

### selenium chromdriver.exe must be in the same directory as this script
driver =  webdriver.Chrome('chromedriver.exe') 

url = ''
username = ''
password = ''

###=======VERY IMPORTANT: DECLARATION OF DISTRICTS TO BE DOWNLOADED

## ---- FOR districts_selection_type
## 'all' =  download all districts' data
## 'range' = only download data for a specific range of districts from  districts' list; i.e: the first 50 districts
## 'id' = download data for list of specific districts as indicated by ID numbers
districts_selection_type = ''

## ----- FOR districts_selection
## leave as is for 'all' selection type
## use function range() for 'range' selection type; i.e range(12,54) to select the 12th district all the way to the 53rd district (alpahabetical order)
## use list to pass district ids, i.e ['04444441', '111134w', '99990332']
districts_selection = 'all' 

###==================================================================


vars_list = [url, username, password, districts_selection_type, districts_selection]
for var in vars_list:
    if var  == '':
        print "At least one variable is empty! Open this script's file and make sure that the all the following variables have set values: "
        print "\n".join(('url', 'username', 'password', 'districts_selection_type', 'districts_selection'))
        print "After setting ALL variables to desired values, Re-run script."
        del vars_list
        sys.exit()

del vars_list

driver.get(url)
driver.find_element_by_name('IDToken1').send_keys(username)
driver.find_element_by_name('IDToken2').send_keys(password)

del url
del username
del password

driver.find_element_by_name('Login.Submit').submit()
driver.find_element_by_xpath('''//*[@id="ctl00_ContentPlaceHolderBodyCenter_divCenterRegion"]/div/div[1]/p/span''').click()

driver.refresh()
time.sleep(10)

districts = driver.find_element_by_id('ddl_district').text.split('\n')
districts = [ district.encode('utf-8') for district in districts[1:]]

if districts_selection_type.lower() == 'all':
    districts = sorted(districts, reverse=True)
    del districts_selection
    del districts_selection_type
elif districts_selection_type.lower() == 'range':
    districts = [districts[i] for i in districts_selection]
    districts = sorted(districts, reverse=True)
    del districts_selection
    del districts_selection_type
elif districts_selection_type.lower() == 'id':
    districts_ids = [re.sub("[(){}<>]",'', district.split(" ")[-1]) for district in districts]
    district_inputs = list(districts_selection)
    district_inputs = [str(district_input) for district_input in district_inputs]
    indexes = [districts_ids.index(district) for district in district_inputs]
    districts = [districts[index] for index in indexes]
    districts = sorted(districts, reverse=True)
    del districts_selection
    del districts_selection_type
else:
    print "Invalid value for 'districts_selection_type' variable; must be either 'all' or 'range' or 'id'"
    del districts_selection
    del districts_selection_type
    sys.exit()
    

driver.refresh()
time.sleep(10)


if len(districts) <= 20:
    for district in districts:
        try:
            Select(driver.find_element_by_id('ddlFileType')).select_by_visible_text('CSV (Comma Separated Values)')
            Select(driver.find_element_by_id('ddl_district')).select_by_visible_text(district)
            driver.find_element_by_id('beginProcess').click()
            time.sleep(3)
        except WebDriverException:
            time.sleep(10)
            continue


    
    driver.refresh()
    time.sleep(15)


    downloadPath =""
    districts = sorted(districts)
    downloaded = []

    for district in districts:
        table = driver.find_elements_by_xpath('''//*[@id="StudentResults"]/tbody/tr''')
        for row in table:
            try:
                if [cell.encode('utf-8') for cell in row.text.split('\n')][0] == district:
                    downloadPath = ''.join(('//*[@id="',row.get_attribute('id').encode('utf-8'),'"]/td[9]/div/a'))
                    driver.find_element_by_xpath(downloadPath).click()
                    print ''.join(( district,' successfully downloaded!'))
                    downloaded.append(district)
                    break
            except StaleElementReferenceException:
                print ''.join((district, " couldn't be downloaded; StaleElementReferenceException error"))
                continue
            except NoSuchElementException:
                print ''.join((district, " couldn't be downloaded; NoSuchElementException error"))
                continue

else:
    
    if len(districts) % 20 == 0:
        pages = len(districts)/20
    else :
        pages = int(len(districts)/20) + 1
    
    districtsCopy = list(districts)
    pageCounter = 1
    downloaded = []
    while pageCounter <= pages:
        driver.refresh()
        time.sleep(20)
        
        if len(districtsCopy) > 20:
            selected_districts = districtsCopy[0:20]
            for district in selected_districts:
                try:
                    Select(driver.find_element_by_id('ddlFileType')).select_by_visible_text('CSV (Comma Separated Values)')
                    Select(driver.find_element_by_id('ddl_district')).select_by_visible_text(district)
                    driver.find_element_by_id('beginProcess').click()
                    time.sleep(3)
                except WebDriverException:
                    time.sleep(10)
                    continue
                
            time.sleep(15)
            driver.refresh()
            time.sleep(10)

            downloadPath =""
            selected_districts = sorted(selected_districts)
            ok = []

            for district in selected_districts:
                table = driver.find_elements_by_xpath('''//*[@id="StudentResults"]/tbody/tr''')
                for row in table:
                    try:
                        
                        if [cell.encode('utf-8') for cell in row.text.split('\n')][0] == district:
                            downloadPath = ''.join(('//*[@id="',row.get_attribute('id').encode('utf-8'),'"]/td[9]/div/a'))
                            driver.find_element_by_xpath(downloadPath).click()
                            print ''.join(( district,' successfully downloaded!'))
                            ok.append(district)
                            break
                    except StaleElementReferenceException:
                        print ''.join((district, " couldn't be downloaded; StaleElementReferenceException error"))
                        continue
                    except NoSuchElementException:
                        print ''.join((district, " couldn't be downloaded; NoSuchElementException error"))
                        continue
            
            downloaded.extend(ok)
            del ok
            del districtsCopy[:20]
            pageCounter+=1
            
        else:
            
            selected_districts = districtsCopy
            for district in selected_districts:
                
                try:
                    Select(driver.find_element_by_id('ddlFileType')).select_by_visible_text('CSV (Comma Separated Values)')
                    Select(driver.find_element_by_id('ddl_district')).select_by_visible_text(district)
                    driver.find_element_by_id('beginProcess').click()
                    time.sleep(3)
                except WebDriverException:
                    time.sleep(10)
                    continue
                
                
            time.sleep(15)
            driver.refresh()
            time.sleep(10)

            downloadPath =""
            selected_districts = sorted(selected_districts)
            ok = []

            for district in selected_districts:
                table = driver.find_elements_by_xpath('''//*[@id="StudentResults"]/tbody/tr''')
                for row in table:
                    try:
                        
                        if [cell.encode('utf-8') for cell in row.text.split('\n')][0] == district:
                            downloadPath = ''.join(('//*[@id="',row.get_attribute('id').encode('utf-8'),'"]/td[9]/div/a'))
                            driver.find_element_by_xpath(downloadPath).click()
                            print ''.join(( district,' successfully downloaded!'))
                            ok.append(district)
                            break
                    except StaleElementReferenceException:
                        print ''.join((district, " couldn't be downloaded; StaleElementReferenceException error"))
                        continue
                    except NoSuchElementException:
                        print ''.join((district, " couldn't be downloaded; NoSuchElementException error"))
                        continue
                        
            downloaded.extend(ok)
            del ok
            del districtsCopy
            pageCounter+=1


driver.refresh()
time.sleep(10)


f = open('output.txt','w')

if len(downloaded) != len(districts):
    
    print f.write('District(s) NOT downloaded:')
    print f.write('  '.join(list(set(districts).difference(downloaded))))
else:
    print f.write('All district(s) successfully downloaded!')
    
    
f.close()
del f
del downloaded

