import os
from flask import Flask, request
from flask_restful import Api
from config.config import DevelopmentEnviroment
from database.database import db

from model.model import init_db

app = Flask(__name__)
app.config.from_object(DevelopmentEnviroment)
db.init_app(app)
# db.create_all()
from controller.user_controller import *
from controller.post_controller import *
#* For initial database intialization
def init_db_main():
	with app.app_context():
		init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
	print(request)
	if request.method == "POST":
		form_data = request.form
		is_success, reason = c_login_validation(form_data['user_id'], form_data['password'])
		if is_success:
			print('validatio complete redirecting to welcome page')
			user_name = form_data['user_id']
			return redirect(url_for('user_home_page'), user_name = user_name)
		else:
			print('user validatio failed')
			print(reason)
			redirect(url_for('login'))

	elif request.method == 'GET':
		return render_template('login.html')

@app.route('/user/<string:user_name>', methods=['GET'])
def user_home_page(user_name):
	return c_user_home_page(user_name)

@app.route('/user/signup', methods=['GET', 'POST'])
def user_sign_up():
	if request.method == 'GET':
		return render_template('signup.html')
	else:
		form_data = request.form
		if c_add_user(form_data):
			print('User added successfully')
			return redirect(url_for('login'))
		else:
			print('addition of user failed')
			print('redirecting again to singup page')
			return redirect(url_for('user_sign_up'))




@app.route('/user/no_user_found', methods=['GET'])
def no_user_found():
	return c_no_user_found()


if __name__ == "__main__":
	init_db_main()
	app.run()
	print('applicatio started')