#!/usr/bin python3

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
from controller.misc_funtionalities import *
from model.model import init_db
from flask_jwt_extended import JWTManager

import worker
# import celery_job_demo
# import celery_tasks

from time import perf_counter_ns
#caching function

from flask_caching import Cache

import yaml
celery = None
cache = None
is_jinja_mode = False
db_file = ""
def set_config():
	global is_jinja_mode, db_file
	with open('project_config.yaml') as file:
		doc = yaml.full_load(file)
		is_jinja_mode = doc['jinja_mode']
		db_file = doc['db_file']
		




def generate_random_key():
	import secrets 
	res = secrets.token_hex()
	return res

def set_upload_folder():
	cwd = os.getcwd()
	UPLOAD_FOLDER = cwd
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
app.config['JWT_SECRET_KEY'] = generate_random_key()
#*Celery worker
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"
app.config["REDIS_URL"] = "redis://localhost:6379"
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_POST"] = 6379
app.config["cache"] = "RedisCache"
'''
CACHE_REDIS_DB=0
CACHE_REDIS_URL=redis://redis:6379/0
CACHE_DEFAULT_TIMEOUT=500
'''
app.config["CACHE_REDIS_DB"]=0
app.config["CACHE_REDIS_URL"]="redis://localhost:6379/0"
app.config["CACHE_DEFAULT_TIMEOUT"]=500

celery = worker.celery
celery.conf.update(
	broker_url = app.config["CELERY_BROKER_URL"],
	result_backend = app.config["CELERY_RESULT_BACKEND"] 
)
celery.conf.timezone= 'Asia/Kolkata'
celery.Task = worker.ContextTask
app.app_context().push()
#*caching
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})
app.app_context().push()
# with app.app_context():
# 	cache.set(cKey, data)
jwt =  JWTManager(app)
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
		initialize_list_recent_post()

def is_user_in_session(user_id:str)->bool:
	print('sesssion is:', session)
	print('user_id receving as:', user_id)
	return user_id in session.keys()
@cache.cached(timeout=2000)
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
		if c_is_admin_user(user_id):
			# following_list = user_manager.get_all_uesr()
			# posts = c_get_home_page_post(user_id, following_list)
			return redirect(url_for('admin_home_page', admin_id= user_id))
		else:
			following_list = c_get_user_following_list(user_id)
			posts = c_get_home_page_post(user_id, following_list)
			u_posts = c_get_user_post(user_id)
			posts.extend(u_posts)
			posts.sort(reverse=True)
		user = create_user_container(user_id)
		return render_template('user_home_jinja.html', user_id = user_id, fname= user_id, posts= posts, user= user)
	else:
		print('no current user found redirecting to login page')
		return redirect(url_for('signin'))


@app.route('/admin/<string:admin_id>', methods=['GET'])
def admin_home_page(admin_id):
	flash('welcome admin')
	raw_users = user_manager.get_all_uesr()
	users = []
	for r_u in raw_users:
		u_obj = create_user_container(r_u.user_id)
		users.append(u_obj)
	return render_template('admin_home_page.html', users = users, admin_id= admin_id)

@app.route('/admin/delete/<string:admin_id>/<string:user_id>', methods=['GET'])
def admin_delete_user(admin_id, user_id):
	print('adminId:', admin_id, " user id:", user_id)
	if c_is_admin_user(admin_id) and admin_id in list(session.keys()):
		posts = c_get_user_post(user_id)
		for p in posts:
			try:
				is_success, err = c_delete_post(user_id, p.post_id)
				if not is_success:
					print('unable to remove post', err)
			except Exception as e:
				print('exception arrived while removing posts', e)
				print(p)
		print('admin verification complete deleting user',)
		print(c_delete_user(user_id), 'delete result')
	return redirect(url_for('admin_home_page', admin_id= admin_id))

@app.route('/admin/profile/view/<string:admin_id>/<string:user_id>', methods=['GET'])
def admin_view_profile(admin_id, user_id):
	u_d = c_get_user_details(user_id)
	posts = c_get_user_post(user_id)
	user = create_user_container(admin_id)
	return render_template('admin_profile_view.html', user_id= user_id, profile = u_d, posts = posts, admin_id=admin_id, user= user)	

@app.route('/admin/profile/delete/post/<string:admin_id>/<string:user_id>/<string:post_id>', methods=['GET'])
def admin_delete_post(admin_id, user_id, post_id):
	is_success, warn = c_delete_post(user_id, post_id)
	if not is_success:
		flash(warn)
	return redirect(url_for('admin_view_profile', admin_id=admin_id, user_id=user_id))

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
	user = create_user_container(user_id)
	return render_template('user_profile.html', user_id= user_id, profile = u_d, posts = posts, user = user)

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
			return redirect(url_for('user_profile', user_id= user_id))
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
	posts = c_update_user_like_dislike_flags(user_id, posts)
	user = create_user_container(user_id)
	return render_template('view_user_profile.html', user_id= user_id, profile = u_d, posts = posts, view_id = view_id, user= user)




@app.route('/user/search/<string:user_id>', methods=['GET'])
def search(user_id:str):
	try:
		print(request.args)
		query = request.args['search']
		# form_data = request.form
		print('search query received for:', query)
		user_list = get_user_list_by_name(query)
		# print(*user_list, sep='\n')
		u_f_l = c_get_raw_user_following_list(user_id)
		l_f_id = [x.following_id for x in u_f_l]
		# print('user_following id', l_f_id)
	except Exception as e:
		print('exception arrived', e)
	# return redirect(url_for('user_home_page', user_id= user_id))
	# return redirect(url_for('create_post', user_id=user_id))
	user = create_user_container(user_id)
	return render_template('search_result.html', user_id= user_id, users= user_list, user_following_list = l_f_id, user= user)


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
	
@app.route('/user/profile/follower/<string:user_id>', methods=['GET'])
def follower_page(user_id):
	print('getting following list')
	f_l = c_get_user_follower_list(user_id)
	u_f_l = c_get_raw_user_following_list(user_id)
	l_f_id = [x.following_id for x in u_f_l]
	user = create_user_container(user_id)
	return render_template('search_result.html', user_id= user_id, users= f_l, user_following_list = l_f_id, user = user)

@app.route('/user/profile/following/<string:user_id>', methods=['GET'])
def following_page(user_id):
	print('getting following list')
	f_l = c_get_user_following_list(user_id)
	u_f_l = c_get_raw_user_following_list(user_id)
	l_f_id = [x.following_id for x in u_f_l]
	user = create_user_container(user_id)
	return render_template('search_result.html', user_id= user_id, users= f_l, user_following_list = l_f_id, user= user)

@app.route('/update/<string:user_id>/profile', methods=['GET', 'POST'])
def edit_user_profile(user_id:str):
	if request.method == "GET":
		user_obj = create_user_container(user_id)
		return render_template('profile_edit.html', user_id= user_id, user_obj = user_obj)
	else:
		print('receving form')
		file_d = request.files
		form_data = request.form
		is_sucss, reason = c_edit_user(user_id, form_data, file_d)
		if not is_sucss:
			flash(reason)
		return redirect(url_for('user_profile', user_id=user_id))

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

# @app.route('/test/search')
# @cache.cached(timeout=3000)
# def te():
# 	job= celery_job_demo.just_say_hello.delay("hi")
# 	print(str(job))
# 	return str(job), 200
	# return render_template('search_result.html')
#* API Work starting here
#* Adding post Api

# @app.route('/something')
# def celery():
# 	job = celery_tasks.setup_periodic_tasks.delay()


#* Updating according to requirements 
#! DEPRICATED
# from Api.post_api import PostLikeApi
# api.add_resource(PostLikeApi, "/api/like", "/api/like/<string:liker_id>/<string:post_id>")

# from Api.post_api import PostFlagApi
# api.add_resource(PostFlagApi, "/api/flag", "/api/flag/<string:flager_id>/<string:post_id>")

# from Api.user_follow_api import FollowApi
# api.add_resource(FollowApi, '/api/follow', '/api/follow/<string:user_id>/<string:f_user_id>')

# from Api.user_control_api import UserControlApi
# api.add_resource(UserControlApi, '/api/user/make_admin', '/api/user/make_admin/<string:user_id>')

# from Api.user_control_api import GetUserPostList
# api.add_resource(GetUserPostList, '/api/user/get_post_list', '/api/user/get_post_list/<string:user_id>')

# from Api.post_api import PostCRUDApi
# api.add_resource(PostCRUDApi, '/api/get_post_details', '/api/user/get_post_details/<string:user_id>/<string:post_id>')


#! Depricated
#* API v2 starting from here
#TODO: Comment API
#* POST API version V2 starting from here

from Api.test_api import TestApi
api.add_resource(TestApi, '/api/test', '/api/test')
#USER API
from Api.user_control_api import UserAuthenticationApi
api.add_resource(UserAuthenticationApi, '/api/v2/user/authentication/', '/api/v2/user/authentication')

from Api.user_control_api import UserManagerApi
api.add_resource(UserManagerApi, '/api/v2/user/create', '/api/v2/user/create')


from Api.user_control_api import UserDetailFetchApi
api.add_resource(UserDetailFetchApi, '/api/v2/user/fetch', '/api/v2/user/fetch/<string:user_id>')

from Api.user_control_api import FetchUserPostList
api.add_resource(FetchUserPostList, '/api/v2/user/post', '/api/v2/user/post/<string:user_id>')

from Api.user_control_api import UserSearchList
api.add_resource(UserSearchList, '/api/v2/user/search', '/api/v2/user/search')

from Api.user_follow_api import FollowUserApi2
api.add_resource(FollowUserApi2, '/api/v2/user/follow', '/api/v2/user/follow')

#getting follow following list
from Api.user_follow_api import GetUserFollowerList
api.add_resource(GetUserFollowerList, '/api/v2/follower/user', '/api/v2/follower/user/<string:user_id>')

from Api.user_follow_api import GetUserFollowingList
api.add_resource(GetUserFollowingList, '/api/v2/following/user', '/api/v2/following/user/<string:user_id>')

from Api.user_control_api import DeleteUser
api.add_resource(DeleteUser, '/api/v2/delete/user', '/api/v2/delete/user/<string:user_id>')

from Api.user_control_api import UpdateUserPassword
api.add_resource(UpdateUserPassword, '/api/v2/passwd/update/user', '/api/v2/passwd/update/user/<string:user_id>')

#POST API
from Api.post_api import PostApiV2
api.add_resource(PostApiV2, '/api/v2/post/', '/api/v2/post/<string:user_id>/<string:post_id>')

from Api.post_api import PostLikeApiV2
api.add_resource(PostLikeApiV2, '/api/v2/like/post', '/api/v2/like/post/<string:user_id>/<string:post_id>')

from Api.post_api import PostFetchApi
api.add_resource(PostFetchApi, '/api/v2/fetch/post', '/api/v2/fetch/post')

from Api.post_api import PostCommentApiV2
api.add_resource(PostCommentApiV2, '/api/v2/comment/post', '/api/v2/comment/post/<string:user_id>/<string:post_id>')

from Api.post_api import PostCarouselApi
api.add_resource(PostCarouselApi, '/api/v2/carousel', '/api/v2/carousel')

from Api.post_api import PostBookmarkApi
api.add_resource(PostBookmarkApi, '/api/v2/bookmark/post', '/api/v2/bookmark/post/<string:user_id>')

from Api.export_api import ExportApi
api.add_resource(ExportApi, '/api/v2/export', '/api/v2/export/<string:user_id>')




if __name__ == "__main__":
	set_config()
	init_db_main()
	# initialize_list_recent_post()
	app.run(host="0.0.0.0")
	print('applicatio started')