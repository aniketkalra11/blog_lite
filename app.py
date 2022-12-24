import os
from flask import Flask, request, session, flash
from flask_session import Session
from flask_restful import Api, Resource
from config.config import DevelopmentEnviroment
from database.database import db
#for file system
from werkzeug.utils import secure_filename
from controller.user_controller import *
from controller.post_controller import *
from model.model import init_db

def generate_random_key():
	import secrets 
	res = secrets.token_hex()
	return res

def set_upload_folder():
	cwd = os.getcwd()
	UPLOAD_FOLDER = os.path.join(cwd, 'resource')
	print(UPLOAD_FOLDER)
	if not os.path.exists(UPLOAD_FOLDER):
		print('creating folder')
		os.mkdir(UPLOAD_FOLDER)
	print(UPLOAD_FOLDER)
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



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

#* For initial database intialization
def init_db_main():
	with app.app_context():
		print('calling init db')
		init_db()

def is_user_in_session(user_id:str)->bool:
	print('sesssion is:', session)
	print('user_id receving as:', user_id)
	return user_id in session.keys()

@app.route('/', methods=['GET', 'POST'])
def signin():
	set_upload_folder()
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
		following_list = c_get_user_following_list(user_id)
		posts = c_get_post_for_user(user_id, following_list)
		return render_template('user_home_jinja.html', user_id = user_id, fname= user_id, posts= posts)
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

@app.route('/user/profile/<string:user_id>', methods=['GET'])
def user_profile(user_id):
	return render_template('user_profile.html')

@app.route('/user/post/<string:user_id>/create_post', methods=['GET', 'POST'])
def create_post(user_id):
	print('post_request receiving')
	if is_user_in_session(user_id):
		if request.method == 'GET':
			return render_template('create_post.html', user_id = user_id)
		else:
			form_data = request.form
			file = request.files['image']
			print(file)
			is_success, reason = c_create_post(user_id, form_data, file)
			if not is_success:
				flash(reason)
			# return redirect(url_for('user_home_page', user_id = user_id))
			return redirect(url_for('create_post', user_id= user_id))
	else:
		print('no user in session redirecting to signup page')
		return redirect(url_for('signin'))

@app.route('/user/post/<string:user_id>/<string:post_id>', methods=['POST'])
def add_post_comment(user_id, post_id):
	print('add comment request received')
	print('user_id:', user_id, 'post_id:', post_id)
	comment = request.form['content']
	print('comment received as:', comment)
	is_success, reason = c_add_comment(user_id, post_id, comment)
	if not is_success:
		flash(reason)
	return redirect(url_for('user_home_page', user_id= user_id))
		
@app.route('/user/jinja', methods=['GET'])
def ji():
	dict_data = {}
	user_id = 'ani'
	post_id = '123'
	dict_data['user_id'] = 'ani'
	dict_data['post_id'] = '123'
	dict_data['list_post'] = ['123', '234', '456']
	posts = []
	users = user_manager.get_all_uesr()
	print('all user received as:', users)
	posts = c_get_post_for_user(user_id, users)
	print('receving posts as' + str(posts))
	return render_template('user_home_jinja.html', input_data= dict_data, user_id = user_id, posts= posts)


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