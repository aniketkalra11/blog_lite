from flask import render_template
from flask import request, abort, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError


from model.user_model_controller import UserModelManager

user_manager = UserModelManager()


# @app.route('/', methods=['GET'])
def c_login(request) -> str:
	print('login request received')
	form_data = request.form
	print(form_data)
	return render_template('login.html')

# def c_login_validation(request) -> str:
# 	print('login validation receiving')
# 	form_data = request.form
# 	print(form_data)
# 	try:
# 		user_name = form_data['user_name'] 
# 		password = form_data['password']
# 		fname = form_data['fname']
# 		lname = form_data['lname']
# 		dob = form_data['dob']
# 		city = form_data['city']
# 		profession = form_data['profession']
# 		# member_type = form_data['member_type']

# 		is_valid, error_str = validate_user_data(user_name, password)
# 		if not is_valid:
# 			raise Exception(error_str)
# 	except KeyError as k_e:
# 		print('Something went wrong key not found')
# 		print(k_e)
# 		abort(500)
# 	except Exception as e:
# 		redirect
# 	try:
# 		# user = UserIdPassword.filter(user_id= user_name, password= password).all()
# 		#TODO: need to change user name to user_id
# 		user = db.session.query(UserIdPassword).filter(UserIdPassword.user_id == user_name and UserIdPassword.password == password).all()
# 		print(user)
# 		# print(user)
# 		if user == None:
# 			print('no user found')
# 			abort(404)
# 		if len(user) == 0:
# 			print('no user found ')
# 			return redirect(url_for('no_user_found'))
# 		# db.session.add(user)
# 		# db.session.commit()
# 	except SQLAlchemyError as sql_error:
# 		print(sql_error)
# 		abort(500)
# 	except Exception as e:
# 		print(e)
# 		abort(500)
# 	print(form_data)
# 	return redirect(url_for('user_home_page', user_name = user_name))


def validate_user_data(user_id:str, password:str) -> tuple:
	if '@' not in user_id:
		return (False, "@ not present in user id")
	if '-' in user_id:
		return(False, ' - not allowed')
	# TODO: need to added regex check in this case
	# TODO: need to verify password at backend
	return (True, '')



def c_user_home_page(user_name):
	print('user_home page')
	return render_template('user_home.html', user_name = user_name)

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
		dob = form_data['dob']
		city = form_data['city']
		profession = form_data['profession']
		if profession != "":
			db_result = user_manager.add_user(userId= user_id, password= password, 
											fname= fname, lname= lname, dob= dob, city= city, profession= profession)
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