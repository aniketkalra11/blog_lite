from datetime import datetime, timedelta
import pytz
from controller.user_controller import *
from controller.post_controller import *
from model.misc_utils import getTodaysDate
from mail_config import send_email





def daily_reminder():
		'''
		This will retrive all user and send reminder for their logins
		'''
		list_users = user_manager.get_all_user_last_login_time()
		cur_time = datetime.now()

		yesterday = timedelta(days=-1)
		for user in list_users:
			last_login_time = user.last_login_time
			if last_login_time < yesterday:
				user_container = create_user_container(user.user_id)
				print('last login greater than one')
				send_email(user.user_id, '''
				Hello {0}
				you have been not visited for more than 1 one day please 
				login and check the activites
			
				Thank you for using Blog Lite Application
				'''.format(user_container.name))
