from flask import Flask, render_template, redirect, url_for, request
from scrape import getLogin, getData, getDetail
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
				return render_template('index.html', error='Login Failed! Please try again.')
	# return render_template('login.html', error=error)

@app.route('/search', methods=['GET', 'POST'])
def search():
	error = None
	if request.method == "POST":
		if request.form['company_name'] != "":
			result, result_type = getData(request.form['company_name'])

			if result == "error":
				error = "Sorry, action is not allowed now! Please try again later!"
				return render_template('search.html', error=error)
			else:
				if result_type == "no_search":
					return render_template('result_number.html', result=result)
				else:
					return render_template('result.html', result=result, company_name=request.form['company_name'])


@app.route('/details', methods=['GET', 'POST'])
def details():
	error = None
	if request.method == "POST":
		if request.form['company_name'] != "":
			
			cr_no = request.form['company_name']
			search_word = request.form['search_word']
			
			print(cr_no)
			result_basic, result_history, result_filings = getDetail(cr_no)

			return render_template('details.html', result_basic = result_basic, result_history=result_history, result_filings=result_filings, search_word=search_word)

@app.route('/intermediate', methods=['GET', 'POST'])
def intermediate():
	pass


if __name__ == '__main__':
	app.run(debug=True)