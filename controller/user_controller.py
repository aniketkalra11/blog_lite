from flask import render_template
from flask import request, abort, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime

from model.user_model_controller import UserModelManager

from datetime import datetime
user_manager = UserModelManager()

class UserContainer():
	def __init__(self, user_id):
		self.user_id = user_id
		user_details = user_manager.get_user_details(user_id)
		self.name = user_details.fname + ' ' + user_details.lname
		# datetime.strftime()
		self.dob = user_details.dob.strftime('%d/%m/%Y')
		print('dob', self.dob)
		self.city = user_details.city
		self.profession = user_details.profession
		self.profile_photo = user_details.profile_photo
		print(self.profile_photo)
		self.num_flwr, self.num_flwing, self.num_post = user_manager.get_user_post_flr_flwing_count(user_id)
		self.follwers = user_manager.get_user_follower_list(user_id)
		self.followings = user_manager.get_user_following_list(user_id)
	def __str__(self):
		s = self.user_id + ' ' + self.name + ' ' + self.dob + ' ' + self.city + ' ' + self.profession
		return s

# @app.route('/', methods=['GET'])
def c_login(request) -> str:
	print('login request received')
	form_data = request.form
	print(form_data)
	return render_template('login.html')


def create_user_container(user_id:str)->UserContainer:
	obj = UserContainer(user_id)
	return obj
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

def c_add_user(form_data) -> list:
	'''
		This function will add user return true if successfully executed
	'''
	# form_data = request.form
	print(form_data)
	db_result = False

	try:
		user_id = form_data['user_id'] 
		if user_id == '':
			# print('empty id received')
			warn_str = 'empty id received'
			return db_result, warn_str
		if user_manager.is_user_exists(form_data['user_id']):
			return False, "User id " + form_data['user_id'] + " already exists"
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
		return db_result, 'Unable to add User please try after some time'
	else:
		printDebug('Successfully added into the database')
		return db_result, ''



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

def c_get_user_following_list(user_id:str)->list:
	result = []
	result = user_manager.get_user_following_list(user_id)
	return result

def c_get_user_details(user_id:str):
	usr_d = create_user_container(user_id)
	printDebug(str(usr_d))
	return usr_d
def printDebug(stat:str)->None:
	print("Controller: ", stat)

def get_user_name(user_id:str)->str:
	u_d = user_manager.get_user_details(user_id)
	# u_d = create_user_container(user_id)
	return str(u_d.fname) + ' ' +str(u_d.lname)


def get_user_list_by_name(name:str)->list:
	n_f = '%{}%'.format(name)
	l = user_manager.get_user_by_name(n_f)
	c_l = []
	for x in l:
		obj = create_user_container(x.user_id)
		c_l.append(obj)
	print('search result', l)
	return c_l