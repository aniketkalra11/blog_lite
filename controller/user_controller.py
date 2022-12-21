from flask import render_template
from flask import request, abort, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime

from model.user_model_controller import UserModelManager

user_manager = UserModelManager()


# @app.route('/', methods=['GET'])
def c_login(request) -> str:
	print('login request received')
	form_data = request.form
	print(form_data)
	return render_template('login.html')



def validate_user_data(user_id:str, password:str) -> tuple:
	if '@' not in user_id:
		return (False, "@ not present in user id")
	if '-' in user_id:
		return(False, ' - not allowed')
	# TODO: need to added regex check in this case
	# TODO: need to verify password at backend
	return (True, '')


def c_no_user_found():
	return render_template('no_user_found.html')

def c_add_user(form_data) -> bool:
	'''
		This function will add user return true if successfully executed
	'''
	# form_data = request.form
	print(form_data)
	db_result = False

	try:
		user_id = form_data['user_id'] 
		if user_id == '':
			print('empty id received')
			return db_result
		password = form_data['password']
		fname = form_data['fname']
		lname = form_data['lname']
		# ('dob', '2022-12-06')
		dob = form_data['dob'].split('-')
		d_dob = datetime(int(dob[0]), int(dob[1]), int(dob[2]))
		city = form_data['city']
		profession = form_data['profession']
		if profession != "":
			db_result = user_manager.add_user(userId= user_id, password= password, 
											fname= fname, lname= lname, dob= d_dob, city= city, profession= profession)
		else:
			db_result = user_manager.add_user(userId= user_id, password= password, 
											fname= fname, lname= lname, dob= dob, city= city)
		log = "Addtion result "+ str(db_result)
		if not db_result:
			raise Exception('unable added into database error from model')
		printDebug(log)
	except Exception as e:
		# print('Controller: Exception arrived during addtion', e)
		printDebug("Exception arrived during addition " + str(e))
		return db_result
	else:
		printDebug('Successfully added into the database')
		return db_result



def c_login_validation(userId:str, password:str)-> list:
	result = []
	if userId == "":
		printDebug('Empty userId received')
		return [False, "empty user Id"]
	if user_manager.is_user_exists(userId):
		print(userId, ' found')
	if user_manager.is_user_pwd_correct(userId, password):
		print(' Validatio complete returing ture')
		return [True, ""]
	else:
		print('incorrect password')
		return [False, "Incorrect Password"]



def printDebug(stat:str)->None:
	print("Controller: ", stat)