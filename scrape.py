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

