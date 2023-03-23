from flask_restful import Resource
from flask_restful import fields, marshal_with, reqparse
from flask import request
from flask_security import auth_required, login_required, roles_accepted, auth_token_required
from flask_jwt_extended import create_access_token


class TestApi(Resource):
		def get(self):
				return {'123': 'Success'}, 200
		def post(self):
			
			return {'token': create_access_token(identity="Something", fresh= True), 'is_success': True}