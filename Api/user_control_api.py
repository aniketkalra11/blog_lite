from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse
from flask_restful import marshal
from model.common_model_object import user_manager
from model.common_model_object import p_m_m
from flask import request
from flask_jwt_extended import create_access_token, jwt_required

from datetime import timedelta
#* Importing controllers
from controller.user_controller import c_login_validation
from controller.user_behaviour_controller import *

from controller.user_controller import *
from controller.post_controller import c_get_home_page_post, c_get_user_post
from .misc_utils import UserApiResponse, create_response
from model.common_model_object import user_behaviour_manager, user_manager
create_parser = reqparse.RequestParser()

create_parser.add_argument('user_id')

class arr_of_post(fields.Raw):
	def output(self, count, d):
		# print('in container a', count)
		# print('in container d', d)
		# print()
		try:
			d = {
				'post_id': d['post_id'],
				'likes': d['likes'],
				'flags': d['flags']
			}
		except Exception as e:
			print('exception arrived during containre', str(e))
		return d

post_id = {
	'post_id': fields.String,
	'likes': fields.Integer,
	'flags': fields.Integer
}

user_post_list = {
	'user_id':fields.String,
	'post_ids': fields.List(arr_of_post)
}

make_admin = {
	'user_id': fields.String,
	'is_success': fields.Boolean
}

class UserControlApi(Resource):
	def make_res_d(self, user_id, response):
		d = {}
		d['user_id'] = user_id
		d['is_success'] = response
		print(d)
		return d

	@marshal_with(make_admin)
	def get(self, user_id):
		result = False
		try:
			print('making user:', user_id, ' As admin')
			result = user_manager.make_user_admin(user_id)
		except Exception as e:
			print(' Exception arrived during execution: ', str(e))
			return 'error', 500
		d = self.make_res_d(user_id, result)
		return d, 201

	@marshal_with(make_admin)
	def delete(self, user_id):
		try:
			print('removing user:', user_id, ' As admin')
			result = user_manager.remove_as_admin(user_id)
		except Exception as e:
			print(' Exception arrived during execution: ', str(e))
			return 'unable to process request', 500
		return self.make_res_d(user_id, result)


class GetUserPostList(Resource):
	def get_post_list(self, user_id:str):
		posts = p_m_m.get_user_post(user_id)
		list_p_d = []
		for p in posts:
			p_i = p_m_m.get_post_interaction(p.post_id)
			if p_i == None:
				continue
			d= { 'likes': p_i.likes, 
						'flags': p_i.flags,
						'post_id': p_i.post_id}
			list_p_d.append(d)
		return list_p_d

	@marshal_with(user_post_list)
	def get(self, user_id):
		if not user_manager.is_user_exists(user_id):
			return 'no user found', 404
		d_posts = self.get_post_list(user_id)
		# print(d_posts)
		d = {
			'user_id': user_id,
			'post_ids': d_posts
		}
		return d, 201


class UserAuthenticationApi(Resource):
	'''
		This class is responsible for user login and token generation and storage of api
	'''
	def post(self):
		print('api request received')
		print('api request', request)
		form = request.get_json()
		user_id = form.get('user_id')
		pwd = form.get('password')
		print("User id received as: ", user_id)
		try:
			print("and Password is: ", pwd)
			result, err = c_login_validation(user_id, pwd)
			expires = timedelta(7)
			token = ''
			if result:
				token = create_access_token(identity=user_id, expires_delta=expires)
				result_token, err = c_add_user_token(user_id, token)
				if not result_token:
					result = False
					token = ''
				else:
					user_container = create_user_container(user_id)
					user_behaviour_manager.update_last_user_login_time(user_id)
			d = {'is_login_success': result, 'token': token, 'error': err, 'user_name': user_container.name}
		except Exception as e:
			print('exception arrived in authentication', e)
			d = {'is_login_success': result, 'token': token, 'error': err}
			return create_response(d, 200, response_type= UserApiResponse.user_authentication)
		print(d)
		return create_response(d, 200, response_type= UserApiResponse.user_authentication)

	def options(self):
		print("receiving options")
		return create_response({}, 200)

	def delete(self):
		print('Logout request receiving')
		try:
			print(request)
			header = request.headers
			json = request.get_json()
			print(json)
			user_id = json['user_id']
			token = header['token']
			print('data retrival complete')
			result , err = c_delete_user_token(user_id, token)
			if result:
				d = {'is_success': True, 'err': ""}
			else:
				d = {'is_success': True, 'err': err}
				return create_response(d, 200, UserApiResponse.user_operation)
			response = create_response(d, 200, UserApiResponse.user_operation)
		except Exception as e:
			print('error arrived during logout', e)
			d = {'is_success': False, 'err': 'unable to create the token'}
			response = create_response(d, 200, UserApiResponse.user_operation)
		return response


class UserManagerApi(Resource):
	def post(self):
		''' this will create a new user in the data base '''
		form_data = request.form
		file = request.files
		print(file)
		print(form_data)
		result, err = c_add_user(form_data=form_data, file= file, image_name='profile_photo')
		d = {
				'is_success': result,
				'err': err 
			}
		if result:
			return create_response(d, 201, UserApiResponse.user_operation)
		else:
			print('error while creating new user', err)
			return create_response(d, 200, UserApiResponse.user_operation)

	def put(self):
		''' This is used to edit existing user '''
		print('put request received')
		try:
			form_data = request.form
			print(form_data)
			user_id = form_data['user_id']
			# token = request.headers['Token']
			# print('token', token)
			file = request.files
			print(file)
			print(form_data)
			# result, err = c_user_token_verification(user_id, token)
			result = True
			d = {}
			if result:
				r, err = c_edit_user(user_id, form_data, file, profile_photo_name='profile_photo')
				if r:
					d= {'is_success': True, 'err': ''}
					return create_response(d, 200, UserApiResponse.user_operation)
				else:
					d = {'is_success': result, 'err': err}
			return create_response({'is_success': result, 'err': err}, 200, UserApiResponse.user_operation)
		except Exception as e:
			print(e)
			return create_response({}, 500)


	def options(self):
		return create_response({}, 200)

class UserDetailFetchApi(Resource):
	'''
	This class will fetch user details
	'''
	def get(self, user_id):
		user_container = c_get_user_details(user_id)
		return create_response(user_container, 200, UserApiResponse.user_details)
	def options(self, user_id):
		return create_response({}, 200)

class FetchUserPostList(Resource):
	'''
		This class will return number the post of user
		Get:- will return dashboard posts,
		Put:- will return profile posts,
	'''
	@jwt_required()
	def get(self, user_id):
		following_list = c_get_user_following_list(user_id)
		posts = c_get_home_page_post(user_id, following_list)
		u_post = c_get_user_post(user_id)
		final_posts = posts + u_post
		final_req_post = []
		for x in final_posts:
			if x.post_type == "public":
				final_req_post.append(x)
		# final_posts.sort(reverse= True)
		final_req_post.sort(reverse=True)
		d = {'user_id': user_id, 'list_post': final_req_post}
		return create_response(d, 200, UserApiResponse.user_dashboard_post_list)

	def options(self, user_id):
		return create_response({}, 200)
	
	@jwt_required()
	def put(self, user_id):
		print('user_id: ', user_id)
		user_posts = c_get_user_post(user_id)
		user_posts.sort(reverse= True)
		try:
			print('Header containt')
			# print(request.headers)
		except Exception as e:
			print('exception arrived', e)
		d= { 'user_id': user_id, 'list_post': user_posts}
		return create_response(d, 200, UserApiResponse.user_dashboard_post_list)


class UserSearchList(Resource):
	''' This Api is responsible for search user and fetch user detials '''
	def post(self):
		''' This will search result and send to the user '''
		try:
			json_obj = request.get_json()
			user_id = json_obj['user_id']
			search_keyword = json_obj['keyword']
		except Exception as e:
			print(json_obj)
			print('exception arrived', e)
			return create_response({}, 500)
		user_list = get_user_list_by_name(search_keyword)
		user_following_list = c_get_user_following_list(user_id)
		c_update_user_container_following_status(user_id, user_list, user_following_list)
		d = {'user_id': user_id, 'search_keyword': search_keyword, 'list_user_container': user_list}
		for x in user_list:
			print(x)
		return create_response(d, 200, UserApiResponse.user_search_result)



	def options(self):
		return create_response({}, 200)
	


class DeleteUser(Resource):
	@jwt_required()
	def post(self, user_id):
		result = user_manager.delete_user(user_id)
		d = {'is_success': True, 'err': ''}
		return create_response(d, 200, UserApiResponse.user_operation)

	def options(self, user_id):
		return create_response({}, 200)
	

class UpdateUserPassword(Resource):
	@jwt_required()
	def post(self, user_id):
		# result = user_manager.delete_user(user_id)
		password = request.form['password']
		new_password = request.form['new_password']
		result, err = c_login_validation(user_id, password)
		if result:
			is_pwd_updated = user_manager.update_user_password(user_id, new_password)
			d = {'is_success': is_pwd_updated, 'err': ''}
		else:
			d = {'is_success': False, 'err': err}
		return create_response(d, 200, UserApiResponse.user_operation)

	def options(self, user_id):
		return create_response({}, 200)