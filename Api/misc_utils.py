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

class ContainerOfLiker(fields.Raw):
		def output(self, key, obj):
			''' This will contain user_id and user_name '''
			try:
				x = obj[key]
				return {
					'liker_name': x.liker_name,
					'time_stamp' : x.time_stamp,
					'liker_id': x.liker_id
				}
			except Exception as e:
				print('exception in like continer', e)
				return {
					'liker_name': '',
					'time_stamp' : '',
					'liker_id': ''
				}


class ContainerOfPostComments(fields.Raw):
		def output(self, key, obj):
				''' This will contain commenter name commenter_id and comment_containt'''

				try:
					x = obj[key]
					temp = {
						'commenter_name' : x.commenter_name,
						'comment_content' : x.comment_content,
						'commenter_id' : x.commenter_id
					}
					return temp
				except Exception as e:
					print('exception ', e)
				return {
						'commenter_name' : '',
						'comment_content' : '',
						'commenter_id' : ''
				}



class ContainerofPostIds(fields.Raw):
		def output(self, key, obj):
				''' This will contain commenter name commenter_id and comment_containt'''
				# print(key, obj)
				# print('obj', obj, ' type', type(obj))
				try:
					x = obj[key]
					temp = {
						'post_id' : x.post_id,
						'timestamp': x.timestamp,
						'is_text_only': True if x.image_url == 'NOT_AVAILABLE' else False
					}
						# d.append(temp)
					return temp 
				except Exception as e:
					print('exception ', e)
				return {
					'post_id': '',
					'timestamp': '',
					'is_text_only': False
				}

class PostApiResponse:

	post_container = {
		'user_id': fields.String,
		'post_id' : fields.String,
		'title' : fields.String,
		'caption' : fields.String,
		'image_url' : fields.String, 
		'timestamp': fields.String,
		'likes': fields.Integer,
		'comment_count': fields.Integer,
		'is_already_liked': fields.Boolean,
		'err': fields.String
	}
	post_operation_result = {
			'post_id' : fields.String,
			'is_success' : fields.String,
			'err': fields.String
	}
	post_like_details = {
		'likes_count': fields.Integer,
		'is_already_liked': fields.Boolean,
		'list_user_likes': fields.List(ContainerOfLiker) #return list of user_ids
	}
	post_like_operation= {
		'is_success': fields.Boolean,
		'like_count': fields.Integer,
		'err': fields.String
	}
	# post_bookmark_details = {
	# 	'bookmark_count': fields.Integer,
	# 	'likers': fields.List(ContainerOfUserIdandUserName) #return list of user_ids
	# }
	post_bookmark_operation= {
			'is_success': fields.Boolean,
			'like_count': fields.Integer,
			'err': fields.String
	},
	post_comments_list = {
		'post_id': fields.String,
		'comments': fields.List(ContainerOfPostComments)
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
	user_details = {
		'user_id': fields.String,
		'profile_photo': fields.String,
		'name': fields.String,
		'numFollowers': fields.Integer,
		'numFollowing': fields.Integer,
		'numPosts': fields.Integer,
		'fname': fields.String,
		'lname': fields.String,
		'dob_d': fields.DateTime,
		'city': fields.String,
		'profession': fields.String
	}
	user_dashboard_post_list ={
		'user_id': fields.String,
		'list_post': fields.List(ContainerofPostIds)
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



