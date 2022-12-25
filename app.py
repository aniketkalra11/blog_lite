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
			flash('Welcome' + str(form_data['user_id']))
			user_name_g = form_data['user_id']
			session[user_name_g] = user_name_g
			print('adding user to session')
			print('addition complete', session)
			return redirect( url_for('user_home_page', user_id = str(user_name_g)))
		else:
			print('user validatio failed')
			flash(reason)
			print(reason)
			# redirect(url_for('login'))
			return redirect(url_for('signin'))

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
		posts = c_get_home_page_post(user_id, following_list)
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
		is_sucess, warn = c_add_user(form_data)
		if is_sucess:
			flash('User added successfully')
			return redirect(url_for('signin'))
		else:
			print('addition of user failed')
			print('redirecting again to singup page')
			flash(warn)
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
	u_d = c_get_user_details(user_id)
	posts = c_get_user_post(user_id)
	print(u_d)
	return render_template('user_profile.html', user_id= user_id, profile = u_d, posts = posts)

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
	try:
		comment = request.form['content']
	except Exception as e:
		flash(str(e))
		return ''
	print('comment received as:', comment)
	is_success, reason = c_add_comment(user_id, post_id, comment)
	if not is_success:
		flash(reason)
	return redirect(url_for('user_home_page', user_id= user_id))


@app.route('/user/profile/<string:user_id>/<string:view_id>', methods=['GET'])
def view_user_profile(user_id:str, view_id:str):
	u_d = c_get_user_details(view_id)
	posts = c_get_user_post(view_id)
	return render_template('view_user_profile.html', user_id= user_id, profile = u_d, posts = posts, view_id = view_id)


@app.route('/user/search/<string:user_id>', methods=['GET'])
def search(user_id:str):
	try:
		print(request.args)
		query = request.args['search']
		# form_data = request.form
		print('search query received for:', query)
		user_list = get_user_list_by_name(query)
		print(*user_list, sep='\n')
	except Exception as e:
		print('exception arrived', e)
	# return redirect(url_for('user_home_page', user_id= user_id))
	# return redirect(url_for('create_post', user_id=user_id))
	return render_template('search_result.html', user_id= user_id, users= user_list)


@app.route('/user/post/<string:user_id>/edit_post', methods=['GET', 'POST'])
def edit_post(user_id):
	print(request.args)
	post_id = request.args['post_id']
	print('edit reques received for post', post_id)
	if request.method == 'GET':
		post = c_get_post_by_post_id(post_id)
		return render_template('edit_post.html', user_id= user_id, post_id= post_id, post = post)
	else:
		form_data = request.form
		file = request.files['image']
		print(file)
		is_success, warn = c_edit_post(user_id, post_id, form_data, file)
		if not is_success:
			flash(warn)
		return redirect(url_for('user_profile', user_id = user_id))


@app.route('/user/post/delete/<string:user_id>/<string:post_id>', methods=['GET'])
def delete_post( user_id, post_id):
	is_success, warn = c_delete_post(user_id, post_id)
	if not is_success:
		flash(warn)
	return redirect(url_for('user_profile', user_id = user_id))
	



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
	posts = c_get_home_page_post(user_id, users)
	print('receving posts as' + str(posts))
	return render_template('user_home_jinja.html', input_data= dict_data, user_id = user_id, posts= posts)

@app.route('/test/search')
def te():
	return render_template('search_result.html')
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