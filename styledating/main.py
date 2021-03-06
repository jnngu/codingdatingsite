from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
	return 'welcome to homepage'

@app.route('/register')
def register():
	return 'welcome to registration page'

@app.route('/code')
def coding_chal():
	return render_template("formpg.html")

@app.route('/process_code', methods=['POST'])
def process_code():
	user_code = request.form['code_submission']
	return "your code was " + user_code

@app.route('/match')
def match():
	return "here are your matches"

@app.route('/chat')
def chat():
	return "welcome to chat"

if __name__ == '__main__':
	app.run(debug=True)