from flask_restful import fields, marshal_with, reqparse
from flask import Response, make_response


class OperationStrings:
		FETCH = "FETCH"
		ADD = "ADD"
		CREATE =  "CREATE"
		PUT = "PUT"
		DELETE = "DELETE"
		POST = "POST"
		LIKE = "LIKE"
		COMMENT = "COMMENT"
		BOOKMARK = "BOOKMARK"
		FLAG = "FLAG"
		combine = lambda str1, str2: str1 + "_" + str2

class ContainerOfUserIdandUserName(fields.Raw):
		def output(self, key, obj):
				''' This will contain user_id and user_name '''
				d = {}
				try:
						d['user_id']= obj['user_id']
						d['user_name'] = obj['user_name']
				except Exception as e:
						print('exception arrived during Container of user Api creation', e)
						return d
				return d
				# return super().output(key, obj)



class PostApiResponse:

	post_container = {
		'post_id' : fields.String,
		'title' : fields.String,
		'containt' : fields.String,
		'img_url' : fields.String, 
		'time_stamp': fields.String,
		'no_of_likes': fields.Integer,
		'no_of_comments': fields.Integer,
		'is_user_already_liked': fields.Boolean,
		'err': fields.String
	}
	post_operation_result = {
			'post_id' : fields.String,
			'is_success' : fields.String,
			'err': fields.String
	}
	post_like_details = {
		'likes_count': fields.Integer,
		'likers': fields.List(ContainerOfUserIdandUserName) #return list of user_ids
	}
	post_like_operation= {
		'is_success': fields.Boolean,
		'like_count': fields.Integer,
		'err': fields.String
	}
	post_bookmark_details = {
		'bookmark_count': fields.Integer,
		'likers': fields.List(ContainerOfUserIdandUserName) #return list of user_ids
	}
	post_bookmark_operation= {
			'is_success': fields.Boolean,
			'like_count': fields.Integer,
			'err': fields.String
	}
	empty = {

	}


class UserApiResponse:
	user_authentication={
		'is_login_success': fields.Boolean,
		'token': fields.String,
		'error': fields.String
	}
	user_operation ={
		'is_success': fields.Boolean,
		'err': fields.String
	}

def set_response_headers(response:Response)->Response:
	print('appending header to response')
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Headers'] = '*'
	response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
	return response



def create_response(response_data:dict, return_code:int, response_type:PostApiResponse = PostApiResponse.empty)->Response:
	print("We have a universal function for everyone")
	@marshal_with(response_type)
	def generate_reponse_data(response_dict:dict):
		return response_dict
	
	final_res_data = generate_reponse_data(response_data)
	response = make_response(final_res_data)
	response.status = return_code
	return set_response_headers(response)



