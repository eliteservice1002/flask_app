from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
from os import path
import os
import time
dirpath = os.getcwd()
chromedriver = os.path.join(dirpath, 'chromedriver.exe')
driver = webdriver.Chrome(executable_path=chromedriver)

def getLogin(username, password):
	
	driver.get('https://www.icris.cr.gov.hk/normal.html')

	window_before = driver.window_handles[0]
	print(window_before)
	time.sleep(3)
	aTag_elements = driver.find_elements_by_tag_name('a')
	aTag_elements[0].click()
	# time.sleep(3)

	# window_mid = driver.window_handles[1]
	# driver.switch_to.window(window_mid)
	# driver.set_window_position(-10000,0)

	window_after = driver.window_handles[2]
	driver.switch_to.window(window_after)
	print(window_after)

	user_id = driver.find_elements_by_class_name('coyname')[0]
	# user_id.send_keys('demoicris')
	user_id.send_keys(username)
	pwd = driver.find_elements_by_name('password')[0]
	# pwd.send_keys('icris2020')
	pwd.send_keys(password)
	driver.find_element_by_id('CHKBOX_01').click()
	driver.find_elements_by_class_name('button')[0].click()
	# time.sleep(5)
	current_url = driver.current_url
	print(current_url)

	return current_url

def getData(search_key):
	
	menu_search = driver.find_element_by_id('mi_0_0')
	menu_search.click()
	company_search = driver.find_element_by_id('mi_0_1')
	company_search.click()
	time.sleep(2)

	c_name = driver.find_elements_by_class_name('coyname')[0]
	c_name.send_keys(search_key)

	btn_search = driver.find_elements_by_tag_name('input')
	btn_search[6].click()
	# time.sleep(5)

	print(driver.current_url)
	data = driver.find_elements_by_class_name('data')
	
	temp = data[0].text
	temp1 = temp.split('\n')

	def listToString(s):
		str1 = " "
		return (str1.join(s))

	result = []
	number = len(temp1)
	for i in range(1, number):
	    c = temp1[i].split(' ')
	    registration = c[1]
	    if c[len(c)-1] == 'business':
	        active_status = c[len(c)-4:]
	        active_status = listToString(active_status)
	        name_status = c[len(c)-5]
	        company_name = c[2:len(c)-6]
	        company_name = listToString(company_name)
	        hk_company = 'Yes'
	        if 'China' in company_name:
	        	hk_company = 'No'
	        if 'CHINA' in company_name:
	        	hk_company = 'No'

	    else:
	        active_status = c[len(c)-1]
	        name_status = c[len(c)-2]
	        company_name = c[2:len(c)-3]
	        company_name = listToString(company_name)
	        hk_company = 'Yes'
	        if 'China' in company_name:
	        	hk_company = 'No'
	        if 'CHINA' in company_name:
	        	hk_company = 'No'
	        		    
	    result.append([registration, company_name, hk_company, name_status, active_status])

	return result

def getDetail(cr_no):

	url = "javascript:selectCompany('"+cr_no+"', '');"
	result = []

	selected_company = driver.find_element_by_xpath('//a[@href="'+url+'"]')
	selected_company.click()

	print(driver.current_url)
	
	table1 = driver.find_elements_by_tag_name('table')[3]
	table2 = driver.find_elements_by_tag_name('table')[4]
	aa = table1.text
	bb = aa.split('\n')
	cc = table2.text
	dd = cc.split('\n')

	CR_no = bb[0].split(": ")[1]
	company_name = bb[1].split(": ")[1]
	company_type = bb[2].split(": ")[1]
	date_of_incorporation = bb[3].split(": ")[1]
	active_status = bb[4].split(": ")[1]
	remarks = bb[5].split("'")[0].split(": ")[1]
	windingup_mode = bb[6].split("'")[0].split(": ")[1]
	register_of_charges = bb[9].split(": ")[1]
	important_note = bb[10].split(": ")[1]

	result_basic = {"CR_no":CR_no, "company_name":company_name, "company_type":company_type, "date_of_incorporation":date_of_incorporation, "active_status":active_status, "remarks":remarks, "windingup_mode":windingup_mode, "register_of_charges":register_of_charges, "important_note":important_note}


	def listToString(s):
		str1 = " "
		return (str1.join(s))

	history = driver.find_elements_by_tag_name('table')[4].text

	row = history.split("\n")
	result_history = []

	for i in range(1, len(row)):

		effective_date = row[i].split(' ')[0]
		used_name = listToString(row[i].split(' ')[1:])

		dict_history = {"effective_date":effective_date, "used_name":used_name}
		result_history.append(dict_history)

	btnGo = driver.find_elements_by_name('Button')[0]
	btnGo.click()

	btnProceed = driver.find_elements_by_tag_name('input')[5]
	btnProceed.click()

	filing_year = driver.find_elements_by_name('filing_year')[0]
	filing_year.click()
	driver.find_elements_by_tag_name('option')[9].click()
	driver.find_elements_by_tag_name('input')[5].click()

	driver.find_elements_by_tag_name('input')[27].click()

