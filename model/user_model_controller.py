'''
	This will work as the interface between controller and model
	all the database related action are performed by this interface
	it will provide ready to use fuctions using that we will directly add to user
	it will not check any input validation
	*ASSUMING THAT ALL INPUT VALIDATION PERFORMED BY THE CONTROLLER
'''
from datetime import date
from .model import db 
from .model import UserIdPassword
from .model import UserDetails
from .model import UserFollowing
from .model import UserFollowers
from .model import UserPostAndFollowerInfo

class UserModelManager():
	'''
	This class will manage all functionalities and user
	'''
	def __init__(self):
		print('Starting user Manger')
		self.total_user = 0
		# self.user_list = db.session.execute(db.select(UserIdPassword)).all()
		# self.total_user = len(self.user_list)
		# for x in self.user_list:
		# 	print(x, type(x))

	def add_user(self, userId, password, fname, lname, dob, city, profession= None, member_type= 'user') -> bool:
		try:
			print('adding user to Database:', userId)
			user = UserIdPassword(user_id = userId, password = password)
			
			# db.session.add(user)
			print('adding user to session')

			if profession:
				print('profession is available ', profession)
				user_details = UserDetails(fname=fname, lname= lname, dob= dob, city=city, profession= profession)
			else:
				print('profession is not available skipping it')
				(y, m, d) = [int(x) for x in dob.split('-')]

				d_t = date(y, m, d)
				user_details = UserDetails(fname=fname, lname= lname, dob= d_t, city=city)
			db.session.add(user_details)
			print('adding user details')

			u_f_details = UserPostAndFollowerInfo(user_id = userId)
			user.user_details.append(user_details)
			db.session.add(u_f_details)
			print('user additional details')

		except Exception as e:
			print('exception is:', e)
			db.session.rollback()
			print('rollbacking everything')
			return False
		else:
			print('commiting changes')
			db.session.commit()
			self.total_user += 1
			print('total user increased ', self.total_user)
			return True

	def is_user_exists(self, userId:str) -> bool:
		'''
			this Function will check and tell wheather user exists or not
		'''
		user_data = db.session.query(UserDetails).filter_by(user_id = userId).first()
		print(user_data, "user data retrived from userId", userId)
		return True if user_data  else False

	def is_user_pwd_correct(self, userId:str, password:str) -> bool:
		print('for password validation userId receiving as:', userId, 'password as:', password)
		# user_data = db.session.query(UserIdPassword).filter(UserIdPassword.user_id == userId and UserIdPassword.password == password).first()
		user_data = UserIdPassword.query.filter_by(user_id = userId, password= password).first()
		print('user data and password retrived as: ', user_data)
		return True if user_data else False

	def add_user_follower(self, userId:str, followerId:str)-> bool:
		try:
			user_follower = UserFollowers(user_id = userId, follower_id = followerId)
			db.session.add(user_follower)
			print('adding follower details:', userId, 'Follower id:', followerId)
			q_data = db.session.query(UserPostAndFollowerInfo).query(user_id = userId).first()
			if q_data:
				q_data.num_followers = q_data.num_followers + 1
				db.session.add(q_data)
				print('updating follower count', q_data)
			else:
				raise Exception('unable to find data', userId)
		except Exception as e:
			print('exception arrived as e:', e)
			db.session.rollback()
			return False
		else:
			db.session.commit()
			print('follower commit successful')
			return True

	def add_user_following(self, userId:str, followingId:str) -> bool:
		try:
			user_following = UserFollowing(user_id = userId, following_id = followingId)
			db.session.add(user_following)
			print('adding user following', user_following)
			q_data = db.session.query(UserPostAndFollowerInfo).filter_by(user_id = userId).first()
			if q_data:
				q_data.following_id = q_data.following_id + 1
				db.session.add(q_data)
			else:
				raise Exception('unable to find data', userId)
		except Exception as e:
			print('exception arrived in add_user_following as: ', e)
			db.session.rollback()
			return False
		else:
			db.session.commit()
			print('following commit complete')
			return True

	def get_user_follower_list(self, userId:str)-> list:
		user_followers = None
		try:
			user_followers = db.session.query(UserFollowers).filter_by(user_id = userId)
			print(user_followers)
			if len(user_followers) == 0:
				print('no user found')
			return user_followers
		except Exception as e:
			print('error while fetching user_follower: ', user_followers)
			return []

	def get_user_following_list(self, userId:str) -> list:
		user_following = None
		try:
			user_following = db.session.query(UserFollowing).filter_by(user_id = userId)
			print(user_following)
			if len(user_following) == 0:
				print('no user found')
			return user_following
		except Exception as e:
			print('error while fetching user_follower: ', user_following)
			return []

	def get_user_post_flr_flwing_count(self, userId:str)-> tuple:
		user_flr, user_flwing, post_count = 0, 0, 0
		rslt_tuple = None
		try:
			data = db.session.query(UserPostAndFollowerInfo).filter_by(user_id = userId).first()
			if data:
				(user_flr, user_flwing, post_count) = (data.num_followers, data.num_following, data.num_post)
				rslt_tuple = (user_flr, user_flwing, post_count)
			else:
				raise Exception('unable to find data', userId)
		except Exception as e:
			print('exception arrived while executing')
			return (-1, -1, -1)
		else:
			print('result received as:', rslt_tuple)
			return rslt_tuple

	def get_user_details(self, userId:str) -> tuple:
		user_data = db.session.query(UserDetails).query(user_id = userId).first()
		return user_data if user_data else (-1, ) # returning a empty tuple with entry value -1 
