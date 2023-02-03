from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse
from flask_restful import marshal
from model.common_model_object import user_manager
from model.common_model_object import p_m_m
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
		print(d_posts)
		d = {
			'user_id': user_id,
			'post_ids': d_posts
		}
		return d, 201