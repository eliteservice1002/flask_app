from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from os import path
import os
import time

dirpath = os.getcwd()
chromedriver = os.path.join(dirpath, 'chromedriver.exe')
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)
    
driver.set_window_position(-10000,0)
driver.get('https://www.icris.cr.gov.hk/normal.html')
window_before = driver.window_handles[0]
print(window_before)
aTag_elements = driver.find_elements_by_tag_name('a')

aTag_elements[0].click()
# time.sleep(5)
window_after = driver.window_handles[2]
driver.switch_to.window(window_after)
print(window_after)

user_id = driver.find_elements_by_class_name('coyname')[0]
user_id.send_keys('demoicris')
pwd = driver.find_elements_by_name('password')[0]
pwd.send_keys('icris2020')
driver.find_element_by_id('CHKBOX_01').click()
driver.find_elements_by_class_name('button')[0].click()

# time.sleep(5)
#  Log in action finish...

print(driver.current_url)

menu_search = driver.find_element_by_id('mi_0_0')

menu_search.click()
company_search = driver.find_element_by_id('mi_0_1')
company_search.click()
# time.sleep(1)
print(driver.current_url)
    
company_name = 'Coca cola'
c_name = driver.find_elements_by_class_name('coyname')[0]
c_name.send_keys(company_name)

btn_search = driver.find_elements_by_tag_name('input')
btn_search[6].click()
# time.sleep(5)

print(driver.current_url)
data = driver.find_elements_by_class_name('data')
total = len(data)

# for i in range(0, total):
#     print(data[i].text)
    
print(data[0].text)

a = data[0].text
b = a.split('\n')
print(b)

def listToString(s):
    str1 = " "
    return (str1.join(s))


result = []
number = len(b)
for i in range(1, number-1):
    c = b[i].split(' ')
    registration = c[1]
    if c[len(c)-1] == 'business':
        active_status = c[len(c)-4:]
        active_status = listToString(active_status)
        name_status = c[len(c)-5]
        hk_company = c[len(c)-6]
        company_name = c[2:len(c)-7]
        company_name = listToString(company_name)
    else:
        active_status = c[len(c)-1]
        name_status = c[len(c)-2]
        company_name = c[2:len(c)-3]
        company_name = listToString(company_name)
    
#     print(registration, company_name, name_status, active_status)
    result.append([registration, company_name, name_status, active_status])

print(result)

#  Detail page:
url = "javascript:selectCompany('0194145', '');"
selected_company = driver.find_element_by_xpath('//a[@href="'+url+'"]')
selected_company.click()
# time.sleep(3)
print(driver.current_url)

table1 = driver.find_elements_by_tag_name('table')[3]
print(table1.text)
table2 = driver.find_elements_by_tag_name('table')[4]
print(table2.text)

aa = table1.text
bb = aa.split('\n')
print(bb)

cc = table2.text
dd = cc.split('\n')
print(dd)

print(len(bb))
CR_no = bb[0].split(": ")[1]
company_name = bb[1].split(": ")[1]
if ":" in bb[2]:
    company_type = bb[2].split(": ")[1]
    date_of_incorporation = bb[3].split(": ")[1]
    active_status = bb[4].split(": ")[1]
    remarks = bb[5].split("'")[0].split(": ")[1]
    windingup_mode = bb[6].split("'")[0].split(": ")[1]
    register_of_charges = bb[9].split(": ")[1]
    important_note = bb[10].split(": ")[1]
    
else:
    company_type = bb[3].split(": ")[1]
    date_of_incorporation = bb[4].split(": ")[1]
    active_status = bb[5].split(": ")[1]
    remarks = bb[7].split("'")[0].split(": ")[1]
    windingup_mode = bb[8].split("'")[0].split(": ")[1]
    register_of_charges = bb[11].split(": ")[1]
    important_note = bb[12].split(": ")[1]

history = driver.find_elements_by_tag_name('table')[4].text
# print(history)

row = history.split('\n')
for i in range(1,len(row)):
    print(row[i].split(' ')[0])
    print(listToString(row[i].split(' ')[1:]))

btnGo = driver.find_elements_by_name('Button')[0]
btnGo.click()

btnProceed = driver.find_elements_by_tag_name('input')[5]
btnProceed.click()

filing_year = driver.find_elements_by_name('filing_year')[0]
filing_year.click()
driver.find_elements_by_tag_name('option')[9].click()
driver.find_elements_by_tag_name('input')[5].click()

def get_list():
    document_name = []
    filing_date = []
    
    rows = driver.find_elements_by_tag_name('tr')
    contents = rows[12:22]
    # print(rows[13].text)

    for i in range(12,22):
        tmp = rows[i].text
        document_name.append(tmp.split('\n')[1])
        filing_date.append(tmp.split('\n')[2].split(' ')[1])
    
    return(document_name, filing_date)


# print(driver.find_elements_by_tag_name('table')[7].text)
print(get_list())
driver.find_elements_by_tag_name('input')[27].click()

print(get_list())
tempText = driver.find_elements_by_tag_name('input')[28].get_attribute('value')
# print('-------------------------', tempText)

while tempText.split(' ')[0] == 'Next':
    driver.find_elements_by_tag_name('input')[28].click()
    print(get_list())
    tempText = driver.find_elements_by_tag_name('input')[28].get_attribute('value')
    
print('Finish')



#  company particulars

menu_search = driver.find_element_by_id('mi_0_0')
menu_search.click()
company_particulars = driver.find_element_by_id('mi_0_3')
company_particulars.click()


# radioBtn = driver.find_elements_by_name('radioButton')[0]
# radioBtn = driver.find_elements_by_name('radioButton')[1]
# radioBtn.click()

cr_no = driver.find_elements_by_name('CRNo')[0]
cr_no.send_keys('1196976')

# company_name = driver.find_elements_by_name('companyName')[0]
# company_name.send_keys('COCA-COLA BEVERAGES HOLDINGS COMPANY LIMITED')
btnSearch = driver.find_elements_by_tag_name('input')[12]
btnSearch.click()