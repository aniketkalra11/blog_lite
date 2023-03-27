import os
from flask import render_template
from flask import request, abort, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime


from model.common_model_object import user_manager
from model.common_model_object import user_token_manager
from .common_function import *
from datetime import datetime

def c_add_user_token(user_id:str, token:str) -> list:

	result = user_token_manager.add_user_token(user_id, token)
	if result:
			return [True, '']
	else:
		return [False, 'Unable to add token']
	

def c_delete_user_token(user_id:str, token:str) ->list:
	result = user_token_manager.delete_user_token(user_id, token)
	if result:
		return [True, '']
	else:
		return [False, 'Unable to delete token, Something went wrong']


def c_user_token_verification(user_id:str, token:str) ->list:
	result = user_token_manager.is_token_valid(user_id, token)
	if result:
		return True, ""
	else:
		return False , "Invalid token received"