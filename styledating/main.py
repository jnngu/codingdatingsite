from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
	return 'this is home'

@app.route('/register')
def register():
	return 'welcome to registration pg'

@app.route('/code')
def coding_chal():
	return render_template("formpg.html")

@app.route('/process_code', methods=['POST'])
def process_code():
	user_code = request.form['code_submission']
	return ""

@app.route('/match')
def match():
	return "here are your matches"

@app.route('/chat')
def chat():
	return "welcome to chat"

@app.route('/submit_code', methods=['POST'])
def handle_data():
    submittedcode = request.form['code_submission']
    return "you submitted " + submittedcode

if __name__ == '__main__':
	app.run(debug=True)