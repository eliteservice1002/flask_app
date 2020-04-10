from flask import Flask, render_template, redirect, url_for, request
from scrape import getLogin, getData
# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
	return render_template('index.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

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
			result = getData(request.form['company_name'])
		
			return render_template('result.html', result=result, company_name=request.form['company_name'])

@app.route('/details', methods=['GET', 'POST'])
def details():
	error = None
	if request.method == "POST":
		company_name = request.form['company_name']
		
		print(company_name)
		return render_template('details.html', result = company_name)

if __name__ == '__main__':
	app.run(debug=True)