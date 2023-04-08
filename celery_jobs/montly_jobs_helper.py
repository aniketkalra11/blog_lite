from datetime import datetime, timedelta
import pytz
from controller.user_controller import *
from controller.post_controller import *
from model.misc_utils import getTodaysDate, getCurDateTime

UTC = pytz.utc

IST = pytz.timezone('Asia/Kolkata')
monthly_time_delta = timedelta(weeks=4)

def utc_to_local(utc_dt:datetime)->str:
	local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(IST)
	datetime_ist = IST.normalize(local_dt)
	return datetime_ist.strftime('%d:%m:%Y-%H:%M:%S')

def monthly_report(user_id:str)->list:
	''' return user montly progress report'''
	'''
		What i am going to show 
		1. Total number of likes received on total post
		2. Total number of comments received on total post
		3. list of post created
	'''
	print('creating monthly progress report')
	list_final_post = []
	total_likes = 0
	total_comments = 0
	total_post_count = 0
	#taking post for one month older
	current_date = getCurDateTime()
	print('Todays date is:', current_date)
	report_start_date = current_date - monthly_time_delta
	print('Older dates:', report_start_date)
	list_user_post = c_get_user_post(user_id)

	for x in list_user_post:
		if x.time_stamp_dt >= report_start_date:
			list_final_post.append(x)
			total_likes += x.likes
			total_comments += len(x.comments)
	total_post_count = len(list_final_post)
	result_container = [list_final_post, total_likes, total_comments, total_post_count]
	return result_container




