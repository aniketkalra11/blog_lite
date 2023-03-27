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
				d = []
				for x in obj:
					temp = {
						'liker_name': x.liker_name,
						'time_stamp' : x.time_stamp,
						'liker_id': x.liker_id
					}
					d.append(temp)
				# try:
				# 		d['user_id']= obj['user_id']
				# 		d['user_name'] = obj['user_name']
				# except Exception as e:
				# 		print('exception arrived during Container of user Api creation', e)
				# 		return d
				return d
				# return super().output(key, obj)


class ContainerOfPostComments(fields.Raw):
		def output(self, key, obj):
				''' This will contain commenter name commenter_id and comment_containt'''
				d = []
				print(key, obj)
				print('obj', obj, ' type', type(obj))
				try:
					for x in obj:
						temp = {
							'commenter_name' : x.commenter_name,
							'comment_content' : x.comment_content,
							'commenter_id' : x.commenter_id
						}
						d.append(temp)
				except Exception as e:
					print('exception ', e)
				return d
				# try:
				# 		d['commenter_name']= obj['commenter_name']
				# 		d['comment_content'] = obj['comment_content']
				# 		d['commenter_id'] = obj['commenter_id']
				# except Exception as e:
				# 		print('exception arrived during Container of post comment Api creation', e)
				# 		return d


class ContainerofPostIds(fields.Raw):
		def output(self, key, obj):
				''' This will contain commenter name commenter_id and comment_containt'''
				print(key, obj)
				print('obj', obj, ' type', type(obj))
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



