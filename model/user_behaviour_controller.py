
from datetime import datetime
from datetime import date
from .model import db
from .model import UserActiveTime
from .model import LastUserLoginTime
from .misc_utils import getCurDateTime, getTodaysDate

class LastLoginTimeNotFoundException(Exception):
	def __init__(self, err_str):
		super().__init__(err_str)
		print("ERROR: Last  Login Time not found exception critical error arrived")


class UserBehaviourController:
		'''
				This controller basically resposnsible for the basic adding the active time and 
				how much time user is spending on the website
				#* ALGORITHM
				1. User last login time is considered when user hit the logout button 
				2. else: if user is not active for more than 10 min then it is considered as offline and last login time will be updated accordingly
				#* How we are going to check wheather a user is active or not
				1. when ever a user requested for some resource or do any action which require any server hit.
				2. then user time will be updated and there will be one timer is running in the background which will take care all the active user and maintain a list for them
				3. if user active time is greater than 10 min then appropriate action will be performed and user will be removed from active list.
				TODO: pending login actions 
				1. when ever your login detected check whether user has login before or not
				if user already login then increment the counter otherwise add entry into the able
		'''
		def __init__(self):
				print('UserBehaviourController: class starting')

		def get_last_user_login_time(self, user_id:str) -> datetime:
			user_last_time = LastUserLoginTime.query.filter_by(user_id).first()
			if user_last_time:
				return user_last_time
			else:
				raise LastLoginTimeNotFoundException(user_id+ " Not found in the current directory please handle this grasefully")


		def update_last_user_login_time(self, user_id:str, time_stamp:datetime= getCurDateTime()) -> bool:
			print('updating usre last logintime')
			last_time = db.session.query(LastUserLoginTime).filter_by(user_id = user_id).first()
			if last_time:
				last_time.time_stamp = time_stamp
			else:
				db.session.rollback()
				print("ERROR: unable to fetch the user id from the current user")
				return False
			db.session.commit()
			print("last login details update complete")
			return True

		def update_user_active_time(self, user_id:str, active_time:int, date:date = getTodaysDate()) -> bool:
			print("UserBehvaiourController: " + "updating user", user_id, " with time:", active_time)
			user_time = db.session.query(UserActiveTime).filter_by(user_id = user_id, date = date).first()
			if user_time:
				user_time.active_time = active_time
				db.session.add(user_time)
			else:
				db.session.rollback()
				print("UserBehaviourController: ERROR , Unable to fetch user with current date")
				print("UserBehaviourController: ***Check whether intialization occured or not")
				return False
			user_time.commit()
			return True


		def add_user_login_for_cur_date(self, user_id:str, date:date = getTodaysDate()) -> bool:
			print('Adding user: ', user_id, " to current date: ", date)
			user_active_time = UserActiveTime(user_id= user_id, date= date)
			try:
				print("Adding session to database started")
				db.session.add(user_active_time)
			except Exception as e:
				db.session.rollback()
				print('Exception arrived unable to add user error as:', e)
				return False
			else:
				print('date added successfully')
				db.session.commit()
				return True

		def is_user_active_on_date(self, user_id:str, date:date) -> bool:
			u_active = db.session.query(UserActiveTime).filter_by(user_id = user_id, date = date).first()
			return True if u_active else False


