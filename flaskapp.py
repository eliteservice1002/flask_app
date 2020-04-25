from flask import Flask, render_template, redirect, request, json
from scrape import getLogin, getData, getDetail, Logout, getParticulars
# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'demoicris' or request.form['password'] != 'icris2020':
			error = 'Invalid Credentials. Please try again.'
			return render_template('index.html', error=error)
		else:
			current_url = getLogin(request.form['username'], request.form['password'])
			if current_url == 'https://www.icris.cr.gov.hk/csci/login_s.do':
				return render_template('search.html')
			else:
				return render_template('index.html', error='Login Failed! Please try again later.')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	error = None
	msg = Logout()
	return redirect('/', code=302)

@app.route('/search', methods=['GET', 'POST'])
def search():
	error = None
	if request.method == "POST":

		if request.form['company_name'] != "":
			print('company_name---------', request.form['company_name'])

			result, result_type = getData(request.form['company_name'])
			print('RESULT_TYPE*****', result_type)

			if result == "error":
				error = "Sorry, Network error happened! Please log out and try to log in again."
				return render_template('search.html', error=error)
			else:
				if result_type == "no_search":
					cr_no = request.form['company_name']
					return render_template('result_number.html', result=result, cr_no=cr_no)
				else:
					return render_template('result.html', result=result, company_name=request.form['company_name'])
		else:
			error = "Please input company name or cr number. "
			return render_template('search.html', error=error)
	else:

		error = "Request Failed. Please try again."
		return render_template('search.html', error=error)

@app.route('/details', methods=['GET', 'POST'])
def details():
	error = None
	if request.method == "POST":
		if request.form['company_name'] != "":
			
			cr_no = request.form['company_name']
			search_word = request.form['search_word']
			print('Search Word:----------', search_word)
			
			result_basic, result_history, result_filings = getDetail(cr_no)
			print("Basic info:-----------", result_basic)

			return render_template('details.html', result_basic = result_basic, result_history=result_history, result_filings=result_filings, cr_no=cr_no, search_word=search_word)

		else:

			error = "Please click the company name correctly! Now no company selected!"
			return render_template('result.html', error=error)


@app.route('/intermediate', methods=['GET', 'POST'])
def intermediate():
	error = None
	print('CR_NO:-----', request.form['cr_no'])

	if request.method == "POST":
		if request.form['cr_no'] != "":
			cr_no = request.form['cr_no']

			result, msg = getParticulars(cr_no)

			if msg == "error":
				error = "Insufficient"
				return error
			elif msg == "network error":
				error = "Network"
				return error
			else:
				return json.dumps({'status':'OK', 'result':result})


if __name__ == '__main__':
	app.run()