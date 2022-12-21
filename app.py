import os
from flask import Flask, request, session
from flask_session import Session
from flask_restful import Api, Resource
from config.config import DevelopmentEnviroment
from database.database import db

from model.model import init_db
def generate_random_key():
	# import string
	# import random
	
	# # initializing size of string
	# N = 10
	
	# # using random.choices()
	# # generating random strings
	# res = ''.join(random.choices(string.ascii_uppercase +
    #                          string.digits, k=N))
	import secrets 
	res = secrets.token_hex()
	return res

app = Flask(__name__)
app.config.from_object(DevelopmentEnviroment)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem' # neet to check wheather it is useful or not
Session(app)
ran_k = generate_random_key()
print('random key received as:', ran_k)
app.secret_key = ran_k
api = Api(app)
db.init_app(app)

# db.create_all()
from controller.user_controller import *
from controller.post_controller import *
#* For initial database intialization
def init_db_main():
	with app.app_context():
		init_db()

@app.route('/', methods=['GET', 'POST'])
def signin():
	print(request)
	if request.method == "POST":
		form_data = request.form
		print('printing form data', form_data)
		is_success, reason = c_login_validation(form_data['user_id'], form_data['password'])
		if is_success:
			print('validatio complete redirecting to welcome page')
			user_name_g = form_data['user_id']
			session[user_name_g] = user_name_g
			print('adding user to session')
			print('addition complete', session)
			return redirect( url_for('user_home_page', user_id = str(user_name_g)))
		else:
			print('user validatio failed')
			print(reason)
			# redirect(url_for('login'))
			return url_for('no_user_found')

	elif request.method == 'GET':
		print(session.keys())
		user_name = ''
		print(session.keys())
		if list(session.keys()) != []:
			user_name = session[list(session.keys())[0]]
		# return render_template('login.html', user_name= user_name)
		return render_template('signin.html')

@app.route('/user/<string:user_id>', methods=['GET'])
def user_home_page(user_id):
	if user_id in list(session.keys()):
		print('user found logging in to home page')
		return render_template('user_home.html', user_id = user_id, fname= user_id)
	else:
		print('no current user found redirecting to login page')
		return redirect(url_for('signin'))

@app.route('/user/signup', methods=['GET', 'POST'])
def user_sign_up():
	if request.method == 'GET':
		return render_template('signup.html')
	else:
		form_data = request.form
		if c_add_user(form_data):
			print('User added successfully')
			return redirect(url_for('signin'))
		else:
			print('addition of user failed')
			print('redirecting again to singup page')
			return redirect(url_for('user_sign_up'))

@app.route('/user/no_user_found', methods=['GET'])
def no_user_found():
	return c_no_user_found()
# user business logic complete

@app.route('/user/signout/<string:user_id>', methods=['GET'])
def signout(user_id):
	print('signout request received')
	print('sessions are: ', session)
	if user_id in session.keys():
		del session[user_id]
	else:
		print('no user found')
		print('there might be some error ')
	return redirect(url_for('signin'))


#* API Work starting here
#* Adding post Api

from Api.post_api import PostLikeApi
api.add_resource(PostLikeApi, "/api/like", "/api/like/<string:liker_id>/<string:post_id>")

from Api.post_api import PostFlagApi
api.add_resource(PostFlagApi, "/api/flag", "/api/flag/<string:flager_id>/<string:post_id>")

#TODO: Comment API


if __name__ == "__main__":
	init_db_main()
	app.run(host="0.0.0.0")
	print('applicatio started')