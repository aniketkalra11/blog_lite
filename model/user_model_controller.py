'''password
	This will work as the interface between controller and model
	all the database related action are performed by this interface
	it will provide ready to use fuctions using that we will directly add to user
	it will not check any input validation
	*ASSUMING THAT ALL INPUT VALIDATION PERFORMED BY THE CONTROLLER
'''
import hashlib
from datetime import date
from .model import db 
from .model import UserIdPassword
from .model import UserDetails
from .model import UserFollowing
from .model import UserFollowers
from .model import UserPostAndFollowerInfo

from .model import LastUserLoginTime
from .model import UserActiveTime

#Misc functions
from .misc_utils import getCurDateTime, getTodaysDate
# from app import cache

class UserModelManager():
	'''
	This class will manage all functionalities and user
	'''
	def __init__(self):
		print('Starting user Manger')
		self.total_user = 0
		self.DEFUALT_PROFILE = 'profile/default_profile.png'
		# self.user_list = db.session.execute(db.select(UserIdPassword)).all()
		# self.total_user = len(self.user_list)
		# for x in self.user_list:
		# 	print(x, type(x))

	def add_user(self, userId, password, fname, lname, dob, city, profession= None, member_type= 'user', profile_photo = 'profile/default_profile.png') -> bool:
		'''
			This function will create the user and intialize all necessary database with respect to user
			intializing databases are
			1. UserPostAndFollowerInfo
			2. UserDetails
			3. LastUserLoginTime #! This will be maintained by another class
			TODO: Check what else i can update in this file
		'''
		try:
			print('Adding new user started')
			# hash_val = hash(password)
			hash_val = hashlib.sha256(password.encode()).hexdigest()
			print("Hash_value for given password is:", password, " is:", hash_val)
			user = UserIdPassword(user_id = userId, hash_value = hash_val, name = fname)


			if profession:
				print('profession is available ', profession)
				user_details = UserDetails(fname=fname, lname= lname, dob= dob, city=city, profession= profession, profile_photo= profile_photo)
			else:
				print('profession is not available skipping it')
				user_details = UserDetails(fname=fname, lname= lname, dob= dob, city=city, profile_photo= profile_photo)
			db.session.add(user_details)
			print('adding user details')

			u_f_details = UserPostAndFollowerInfo(user_id = userId)
			user.user_details.append(user_details)
			db.session.add(u_f_details)

			#* Adding user last login details
			l_u_active = LastUserLoginTime(user_id= userId)
			user.last_user_login.append(l_u_active)
			db.session.add(u_f_details)
			print("Adding user last login time")
			usr_active_time = UserActiveTime(user_id= userId, date= getTodaysDate())
			user.user_active_time.append(usr_active_time)
			db.session.add(usr_active_time)
			print("user active time on website")
			print('User creation complete')

		except Exception as e:
			print('exception is:', e)
			db.session.rollback()
			print('rollbacking everything')
			return False
		else:
			print('User creation commiting changes')
			db.session.commit()
			self.total_user += 1
			return True

	def is_user_exists(self, userId:str) -> bool:
		'''
			this Function will check and tell wheather user exists or not
		'''
		user_data = db.session.query(UserDetails).filter_by(user_id = userId).first()
		print(user_data, "user data retrived from userId", userId)
		return True if user_data  else False

	def is_user_pwd_correct(self, userId:str, password:str) -> bool:
		#print('for password validation userId receiving as:', userId, 'password as:', password)
		# user_data = db.session.query(UserIdPassword).filter(UserIdPassword.user_id == userId and UserIdPassword.password == password).first()
		# hash_val = hash(password)
		hash_val = hashlib.sha256(password.encode()).hexdigest()
		user_data = UserIdPassword.query.filter_by(user_id = userId, hash_value= hash_val).first()
		#print('user data and password retrived as: ', user_data)
		return True if user_data else False

	def add_user_follower(self, userId:str, followerId:str)-> bool:
		try:
			user_follower = UserFollowers(user_id = userId, follower_id = followerId)
			db.session.add(user_follower)
			#print('adding follower details:', userId, 'Follower id:', followerId)
			q_data = db.session.query(UserPostAndFollowerInfo).filter_by(user_id = userId).first()
			if q_data:
				q_data.num_followers = q_data.num_followers + 1
				db.session.add(q_data)
				#print('updating follower count', q_data)
			else:
				raise Exception('unable to find data', userId)
		except Exception as e:
			#print('exception arrived as e:', e)
			db.session.rollback()
			return False
		else:
			db.session.commit()
			#print('follower commit successful')
			return True

	def add_user_following(self, userId:str, followingId:str) -> bool:
		try:
			user_following = UserFollowing(user_id = userId, following_id = followingId)
			db.session.add(user_following)
			#print('adding user following', user_following)
			q_data = db.session.query(UserPostAndFollowerInfo).filter_by(user_id = userId).first()
			if q_data:
				q_data.num_of_following = q_data.num_of_following + 1
				db.session.add(q_data)
			else:
				raise Exception('unable to find data', userId)
		except Exception as e:
			#print('exception arrived in add_user_following as: ', e)
			db.session.rollback()
			return False
		else:
			db.session.commit()
			#print('following commit complete')
			return True

	def get_user_follower_list(self, userId:str)-> list:
		user_followers = None
		try:
			user_followers = db.session.query(UserFollowers).filter_by(user_id = userId).all()
			#print(user_followers)
			if len(user_followers) == 0:
				# print('no user found')
				pass
			return user_followers
		except Exception as e:
			#print('error while fetching user_follower: ', user_followers)
			return []

	def get_user_following_list(self, userId:str) -> list:
		user_following = []
		try:
			user_following = db.session.query(UserFollowing).filter_by(user_id = userId).all()
			#print(user_following)
			if len(user_following) == 0:
				# print('no user found')
				pass
			return user_following
		except Exception as e:
			#print('error while fetching user_follower: ', user_following)
			return []

	def get_user_post_flr_flwing_count(self, userId:str)-> tuple:
		user_flr, user_flwing, post_count = 0, 0, 0
		rslt_tuple = None
		try:
			data = UserPostAndFollowerInfo.query.filter_by(user_id= userId).first()
			#print('getting user post count', data)
			if data:
				(user_flr, user_flwing, post_count) = (data.num_followers, data.num_of_following, data.num_of_post)
				rslt_tuple = (user_flr, user_flwing, post_count)
			else:
				raise Exception('unable to find data', userId)
		except Exception as e:
			#print('exception arrived while executing', e)
			return (-1, -1, -1)
		else:
			#print('result received as:', rslt_tuple)
			return rslt_tuple

	def get_user_details(self, userId:str) -> tuple:
		user_data = db.session.query(UserDetails).filter_by(user_id = userId).first()
		return user_data if user_data else (-1, ) # returning a empty tuple with entry value -1 

	def get_all_uesr(self) ->list:
		user_list = UserDetails.query.all()
		#print(user_list)
		return user_list

	def get_all_user_last_login_time(self)->list:
		user_list = LastUserLoginTime.query.all()
		return user_list

	def get_user_by_name(self, name:str)->list:
		user_list = []
		l1 = (UserDetails.query.filter(UserDetails.fname.like(name)).all())
		#print('receving name as:', l1)
		l2 = (UserDetails.query.filter(UserDetails.lname.like(name)).all())
		for x in l1:
			if x in l2:
				l2.remove(x)
		#print('receving name as:', l2)
		user_list = l1 + l2
		return user_list
	


	#* edit section starting
	def edit_profile_details(self, user_id:str, fname:str, lname:str, city:str, profession:str, profile_photo:str = None, password:str = None)->list:
		try:
			u_d = self.get_user_details(user_id)
			if password:
				u_d.password = password
			u_d.fname = fname
			u_d.lname = lname
			u_d.city = city
			u_d.profession = profession
			if profile_photo:
				u_d.profile_photo = profile_photo
			db.session.add(u_d)
		except Exception as e:
			return False, 'Unable to Update profile' + str(e)
		else:
			db.session.commit()
			return True, ''
	def update_user_password(self, user_id:str, new_password:str)->bool:
		try:
			u_d = db.session.query(UserIdPassword).filter_by(user_id = user_id).first()
			print('User password update received for:' , u_d.name)
			hash_val  = hashlib.sha256(new_password.encode()).hexdigest()
			u_d.hash_value = hash_val
			db.session.add(u_d)
			db.session.commit()
			return True
		except Exception as e:
			print('exeception arrived during password updation', e)
			return False
		
	#* REMOVE SECTION STARTING HERE

	def remove_user_follower(self, userId:str, followerId:str)->bool:
		try:
			user_follower = UserFollowers.query.filter_by(user_id = userId, follower_id = followerId).first()
			db.session.delete(user_follower)
			#print('adding follower details:', userId, 'Follower id:', followerId)
			q_data = db.session.query(UserPostAndFollowerInfo).filter_by(user_id = userId).first()
			if q_data:
				q_data.num_followers = q_data.num_followers - 1
				db.session.add(q_data)
				#print('updating follower count', q_data)
			else:
				raise Exception('unable to find data', userId)
		except Exception as e:
			#print('exception arrived as e:', e)
			db.session.rollback()
			return False
		else:
			db.session.commit()
			#print('follower commit successful')
			return True

	def remove_user_following(self, userId:str, followingId:str) -> bool:
		try:
			user_following = UserFollowing.query.filter_by(user_id = userId, following_id = followingId).first()
			db.session.delete(user_following)
			#print('adding user following', user_following)
			q_data = db.session.query(UserPostAndFollowerInfo).filter_by(user_id = userId).first()
			if q_data:
				q_data.num_of_following = q_data.num_of_following - 1
				db.session.add(q_data)
			else:
				raise Exception('unable to find data', userId)
		except Exception as e:
			#print('exception arrived in add_user_following as: ', e)
			db.session.rollback()
			return False
		else:
			db.session.commit()
			#print('following commit complete')
			return True

	def make_user_admin(self, user_id:str)->bool:
		user_details = UserDetails.query.filter_by(user_id= user_id).first()
		if user_details:
			user_details.member_type = 'ADMIN'
			db.session.add(user_details)
		else:
			raise Exception('No User Found')
		try:
			db.session.commit()
		except:
			db.session.rollback()
			return False
		return True

	def remove_as_admin(self, user_id:str)->bool:
		user_details = UserDetails.query.filter_by(user_id= user_id).first()
		if user_details:
			user_details.member_type = 'USER'
			db.session.add(user_details)
		else:
			raise Exception('No User Found')
		try:
			db.session.commit()
		except:
			db.session.rollback()
			return False
		return True
	
	def delete_user(self, user_id:str)->bool:
		user_id_pwd = UserIdPassword.query.filter_by(user_id = user_id).first()
		user_f_c = UserPostAndFollowerInfo.query.filter_by(user_id = user_id).first()
		#updating user following follwer count
		user_fing = UserFollowing.query.filter_by(user_id = user_id).all()
		for u in user_fing:
			try:
				#print(u)
				self.remove_user_follower(user_id, u.following_id)
			except Exception as e:
				#print('error otnrason', e)
				pass
		user_flwr = UserFollowers.query.filter_by(user_id = user_id).all()
		for u in user_flwr:
			#print(u)
			try:
				self.remove_user_following(user_id, u.follower_id)
			except Exception as e:
				#print('error stneirasn ', e)
				pass
		if user_id_pwd and user_f_c:
			try:
				db.session.delete(user_id_pwd)
				db.session.delete(user_f_c)
				#print('deleting user: ', user_id)
			except Exception as e:
				#print('exception arrived while deleteing ', e)
				db.session.rollback()
			else:
				#print('chages commited ', user_id)
				db.session.commit()