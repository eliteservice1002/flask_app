from selenium import webdriver

import time

options = webdriver.ChromeOptions()
# options.add_argument('headless') 

driver = webdriver.Chrome(options=options)

def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver


def getLogin(username, password):
	
	driver.get('https://www.icris.cr.gov.hk/normal.html')

	aTag_elements = driver.find_elements_by_tag_name('a')
	aTag_elements[0].click()
	time.sleep(2)
	
	window_after = driver.window_handles[1]
	driver.switch_to.window(window_after)
	print("*************", driver.current_url)
	
	try:
		user_id = driver.find_elements_by_class_name('coyname')[0]
	
		user_id.send_keys(username)
		pwd = driver.find_elements_by_name('password')[0]
		
		pwd.send_keys(password)
		driver.find_element_by_id('CHKBOX_01').click()
		driver.find_elements_by_class_name('button')[0].click()
		
		current_url = driver.current_url
		print("+++", current_url)	

		return current_url

	except:
		driver.quit()
		return ""

def getData(search_key):

	print("Search :   ----- ", driver.current_url)

	if any(char.isdigit() for char in search_key):

		result_type = "no_search"

		try:
			menu_search = driver.find_element_by_id('mi_0_0')
			menu_search.click()
			time.sleep(1)
			company_particulars = driver.find_element_by_id('mi_0_3')
			company_particulars.click()

			cr_no = driver.find_elements_by_name('CRNo')[0]
			cr_no.send_keys(search_key)

			btnSearch = driver.find_elements_by_tag_name('input')[12]
			btnSearch.click()

			basic_info = driver.find_elements_by_tag_name('table')[3]
			
			aa = basic_info.text
			bb = aa.split('\n')

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
				company_name = company_name + "\n" + bb[2]
				
				company_type = bb[3].split(": ")[1]
				date_of_incorporation = bb[4].split(": ")[1]
				active_status = bb[5].split(": ")[1]
				remarks = bb[6].split("'")[0].split(": ")[1]
				windingup_mode = bb[7].split("'")[0].split(": ")[1]
				register_of_charges = bb[10].split(": ")[1]
				important_note = bb[11].split(": ")[1]

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

			result = {'basic':result_basic, 'history':result_history}
			return result, result_type

		except:
			driver.quit()
			return "error", ""

	else: #  Company Name Search
		
		result_type = "name_search"
		print('HERE')

		try:
			menu_search = driver.find_element_by_id('mi_0_0')
			menu_search.click()
			time.sleep(1)
			company_search = driver.find_element_by_id('mi_0_1')
			company_search.click()

			c_name = driver.find_elements_by_class_name('coyname')[0]
			c_name.send_keys(search_key)

			btn_search = driver.find_elements_by_tag_name('input')
			btn_search[6].click()
			# time.sleep(5)

			print(driver.current_url)

			driver.find_elements_by_tag_name('select')[0].click()

			option = driver.find_elements_by_tag_name('option')
			
			result = []

			for i in range(0, len(option)):
			    
			    driver.find_elements_by_tag_name('select')[0].click()
			    driver.find_elements_by_tag_name('option')[i].click()
			    if len(option) != 1:
			    	driver.find_elements_by_tag_name('input')[19].click()
			    
			    data = driver.find_elements_by_class_name('data')

			    temp = data[0].text
			    temp1 = temp.split('\n')

			    def listToString(s):
			    	str1 = " "
			    	return (str1.join(s))

			    if i == (len(option)-1):
			    	
			    	number = len(temp1) - 1
			    else:

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


			return result, result_type
		except:
			driver.quit()
			return "error", ""

def getDetail(cr_no):

	url = "javascript:selectCompany('"+cr_no+"', '');"

	total = len(driver.find_elements_by_tag_name('option'))

	for i in range(0, total):

		driver.find_elements_by_tag_name('select')[0].click()
		time.sleep(1)
		driver.find_elements_by_tag_name('option')[i].click()
		
		try:
			driver.find_elements_by_tag_name('input')[19].click()
		except:
			print('There is no button!!!')

		try:
			selected_company = driver.find_element_by_xpath('//a[@href="'+url+'"]')
			selected_company.click()
			break
		except:
			print('There is no matched link in this page')
			

	print(driver.current_url)
	
	basic_info = driver.find_elements_by_tag_name('table')[3]
	
	aa = basic_info.text
	bb = aa.split('\n')
	

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
		company_name = company_name + "\n" + bb[2]
		
		company_type = bb[3].split(": ")[1]
		date_of_incorporation = bb[4].split(": ")[1]
		active_status = bb[5].split(": ")[1]
		remarks = bb[6].split("'")[0].split(": ")[1]
		windingup_mode = bb[7].split("'")[0].split(": ")[1]
		register_of_charges = bb[10].split(": ")[1]
		important_note = bb[11].split(": ")[1]

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

	result_filings = []

	filing_year = driver.find_elements_by_name('filing_year')[0]
	filing_year.click()
	time.sleep(1)
	driver.find_elements_by_tag_name('option')[9].click()
	driver.find_elements_by_tag_name('input')[5].click()

	def get_list(number):
		
		# status_cn = 0
		document_name = []
		filing_date = []
		rows = driver.find_elements_by_tag_name('tr')

		for i in range(12, 12+number+1):
			tmp = rows[i].text
			try:
				document_name = tmp.split('\n')[1]
				filing_date = tmp.split('\n')[2].split(' ')[1]
				result_filings.append({'document_name':document_name, 'filing_date':filing_date})
			except:
				print('Next row')

	tmp = driver.find_elements_by_tag_name('table')[8].text
	tmp1 = tmp.split('\n')[0]
	
	tmp2 = tmp1.split(' ')
	total = int(tmp2[len(tmp2)-2])
	
	rest = total % 10

	if rest>0:
	    page_no = int(total / 10) + 1
	else:
	    page_no = total / 10


	for i in range(0, page_no):
	    
	    driver.find_elements_by_tag_name('select')[2].click()
	    time.sleep(1)
	    driver.find_elements_by_tag_name('option')[12+i].click()
	    # if page_no != 1:
	    try:
	    	driver.find_elements_by_tag_name('input')[26].click()
	    except:
	    	print('There is no button')
	    
	    if total>10:
	        total=total-10
	        get_list(10)
	    else:
	        get_list(total)
	

	return result_basic, result_history, result_filings

def Logout():
	driver.quit()