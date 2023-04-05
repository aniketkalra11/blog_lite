import os
from flask import render_template
from flask import request, abort, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime

# from model.user_model_controller import UserModelManager
from model.common_model_object import user_manager
from .common_function import *
from datetime import datetime
# user_manager = UserModelManager()
cwd = os.getcwd()
UPLOAD_FOLDER = os.path.join(cwd, 'static' )
print(UPLOAD_FOLDER)
if not os.path.exists(UPLOAD_FOLDER):
    print('creating folder')
    os.mkdir(UPLOAD_FOLDER)
print(UPLOAD_FOLDER)
class UserContainer():
	def __init__(self, user_id):
		self.user_id = user_id
		user_details = user_manager.get_user_details(user_id)
		self.user_details = user_details
		self.fname = user_details.fname
		self.lname = user_details.lname
		
		self.name = user_details.fname + ' ' + user_details.lname
		# datetime.strftime()
		self.dob_d = user_details.dob
		self.dob = self.dob_d.strftime('%d/%m/%Y')
		#print('dob', self.dob)
		self.city = user_details.city
		self.profession = user_details.profession
		self.profile_photo = user_details.profile_photo
		self.user_type = user_details.member_type
		#print(self.profile_photo)
		self.num_flwr, self.num_flwing, self.num_post = user_manager.get_user_post_flr_flwing_count(user_id)
		self.follwers = user_manager.get_user_follower_list(user_id)
		self.followings = user_manager.get_user_following_list(user_id)
		#!duplicating code
		self.numFollowers = self.num_flwr
		self.numFollowing = self.num_flwing
		self.numPosts = self.num_post
		#*latest introduced as per requirements
		self.is_user_already_following = False
	def __str__(self):
		s = self.user_id + ' ' + self.name + ' ' + self.dob + ' ' + self.city + ' ' + self.profession
		return s
	def __eq__(self, a):
		try:
			# return True if self.name == a.name else False
			return True if self.user_id == a.user_id else False
		except:
			return False
	
	def __gt__(self, a):
		return True if self.name > a.name else False

	def __lt__(self, a):
		return True if self.name < a.name else False
	
	def __ge__(self, a):
		return True if self.name >= a.name else False
	
	def __le__(self, a):
		return True if self.name <= a.name else False

# @app.route('/', methods=['GET'])
def c_login(request) -> str:
	#print('login request received')
	form_data = request.form
	#print(form_data)
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

def name_validation(s:str)->bool:
	return s.isalpha()
def save_profile_photo(image, user_id:str, image_name = 'image') -> str:
		profile_photo= None
		file = image[image_name]
		#print(file)
		if file.filename == '':
			print('no profile photo provided continuing with older one')
		else: 
			if allowed_file(file.filename):
				f_name = create_file_name(user_id, file.filename)
				file_dir = os.path.join('profile/',  f_name)
				#print('updated file dir: ',file_dir)
				profile_photo = file_dir
			else:
				print('invalid profile photo received')
				return False, "invalid profile photo received"
		#print('profile photo is:', profile_photo)
			if profile_photo:
				file_dir = os.path.join(UPLOAD_FOLDER, profile_photo)
				#print('updating profile photo', file_dir)
				#print(file)
				try:
					file.save(file_dir)
				except Exception as e:
					print(e)
					os.remove(os.path.join(UPLOAD_FOLDER, profile_photo))
					os.save(file_dir)
				print('profile_photo save success')
				return profile_photo
		return ''

def c_add_user(form_data, file=None, image_name = 'image') -> list:
	'''
		This function will add user return true if successfully executed
	'''
	# form_data = request.form
	#print(form_data)
	db_result = False

	try:
		user_id = form_data['user_id'] 
		user_id.lower()
		if user_id == '':
			# #print('empty id received')
			warn_str = 'empty id received'
			return db_result, warn_str
		if user_manager.is_user_exists(form_data['user_id']):
			return False, "User id " + form_data['user_id'] + " already exists"
		password = form_data['password']
		fname = form_data['fname']
		lname = form_data['lname']
		if not name_validation(fname) or not name_validation(lname):
			return False, 'Name Should be aplhabets only'
		# ('dob', '2022-12-06')
		dob = form_data['dob'].split('-')
		d_dob = datetime(int(dob[0]), int(dob[1]), int(dob[2]))
		city = form_data['city']
		if not name_validation(city):
			return False, 'City Name should not contain any special characters'
		profession = form_data['profession']
		if not name_validation(city):
			return False, 'Profession should not contain any special characters'
		profession_test = lambda prof : prof if prof != "" else None
		if(file and file[image_name] != ''):
			profile_photo = save_profile_photo(file, user_id, image_name= image_name)
			if profile_photo == '':
				return False, 'Unable to save profile photo'
			db_result = user_manager.add_user(userId= user_id,password= password, dob=d_dob, fname= fname, lname =lname, city=city, profession= profession_test(profession), profile_photo= profile_photo)
		else:
			db_result = user_manager.add_user(userId= user_id,password= password, fname= fname, lname =lname, city=city, dob=d_dob, profession= profession_test(profession))
			print('no photo received')
		# if profession != "":
		# 	db_result = user_manager.add_user(userId= user_id, password= password, 
		# 									fname= fname, lname= lname, dob= d_dob, city= city, profession= profession)
		# else:
		# 	db_result = user_manager.add_user(userId= user_id, password= password, 
		# 									fname= fname, lname= lname, dob= d_dob, city= city)
		
		log = "Addtion result "+ str(db_result)
		if not db_result:
			raise Exception('unable added into database error from model')
		printDebug(log)
	except Exception as e:
		# #print('Controller: Exception arrived during addtion', e)
		printDebug("Exception arrived during addition " + str(e))
		return db_result, 'Unable to add User please try after some time'
	else:
		printDebug('Successfully added into the database')
		return db_result, ''



def c_edit_user(user_id,form_data, files, profile_photo_name= 'image') ->list:
		old_details = user_manager.get_user_details(user_id)
		old_image_url = old_details.profile_photo
		# password = form_data['password']
		fname = form_data['fname']
		lname = form_data['lname']
		if not name_validation(fname) or not name_validation(lname):
			return False, 'Name Should be aplhabets only'
		city = form_data['city']
		if not name_validation(city):
			return False, 'City Name should not contain any special characters'
		profession = form_data['profession']
		if not name_validation(city):
			return False, 'Profession should not contain any special characters'
		profile_photo = None
		try:
			file = files[profile_photo_name]
			#print(file)
			if file.filename == '':
				print('no profile photo provided continuing with older one')
			else: 
				if allowed_file(file.filename):
					f_name = create_file_name(user_id, file.filename)
					file_dir = os.path.join('profile/',  f_name)
					#print('updated file dir: ',file_dir)
					profile_photo = file_dir
				else:
					print('invalid profile photo received')
					return False, "invalid profile photo received"
		except Exception as e:
			print('error arrived during image process', e)
		#print('profile photo is:', profile_photo)
		is_success, reason = user_manager.edit_profile_details(user_id, fname, lname, city, profession, profile_photo= profile_photo)
		if is_success:
			if profile_photo:
				file_dir = os.path.join(UPLOAD_FOLDER, profile_photo)
				#print('updating profile photo', file_dir)
				#print(file)
				file.save(file_dir)
				#print('old_image url:', old_image_url)
				if old_image_url != user_manager.DEFUALT_PROFILE:
					#print('removing old profile photo')
					try:
						os.remove(os.path.join(UPLOAD_FOLDER, old_image_url))
					except Exception as e:
						print('unable to remove old photo: ', e)
			return True, ''
		else:
			#print('upadation failed')
			return is_success, reason

def c_login_validation(userId:str, password:str)-> list:
	result = []
	userId.lower()
	if userId == "":
		printDebug('Empty userId received')
		return [False, "empty user Id"]
	if user_manager.is_user_exists(userId):
		print(userId, ' found')
	else:
		return [False, 'User not found']
	if user_manager.is_user_pwd_correct(userId, password):
		#print(' Validatio complete returing ture')
		return [True, ""]
	else:
		#print('incorrect password')
		return [False, "Incorrect Password"]

def c_get_raw_user_following_list(user_id:str)->list:
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

def c_is_admin_user(user_id:str)->bool:
	try:
		u_d = user_manager.get_user_details(user_id)
		return True if u_d.member_type == 'ADMIN' else False
	except:
		return False
	

def get_user_list_by_name(name:str)->list:
	n_f = '%{}%'.format(name)
	l = user_manager.get_user_by_name(n_f)
	c_l = []
	for x in l:
		obj = create_user_container(x.user_id)
		c_l.append(obj)
	#print('search result', l)
	return c_l

def c_get_user_follower_list(user_id:str)->list:
	l = user_manager.get_user_follower_list(user_id)
	r_l = []
	for x in l:
		obj = create_user_container(x.follower_id)
		r_l.append(obj)
	r_l.sort()
	return r_l

def c_get_user_following_list(user_id:str)->list:
	l = user_manager.get_user_following_list(user_id)
	r_l = []
	for x in l:
		obj = create_user_container(x.following_id)
		r_l.append(obj)
	r_l.sort()
	return r_l

def c_update_user_container_following_status(user_id:str, list_users:list, list_followers:list = [] ):
	''' this will update the user follower and following status '''
	''' As per python documentation list_user and list_following are passed by ref then their results are replicated here also '''
	if (list_followers == []):
		list_followers = c_get_user_following_list(user_id)
	for x in list_users:
		for y in list_followers:
			if x == y:
				x.is_user_already_following = True


def c_delete_user(user_id:str)->bool:
	user_details = user_manager.get_user_details(user_id)
	is_success  = user_manager.delete_user(user_id)
	if is_success:
		image_url = user_details.image_url
		if image_url != user_manager.DEFUALT_PROFILE:
			image_dir = os.path.join(UPLOAD_FOLDER, image_url)
			#print(image_dir)
			try:
				os.remove(image_dir)
			except Exception as e:
				print('unable to remove image', e)
	return is_success