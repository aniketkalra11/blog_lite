from datetime import datetime, timedelta
import pytz
from controller.user_controller import *
from controller.post_controller import *
from model.misc_utils import getTodaysDate
from mail_config import send_email
from celery_jobs.montly_jobs_helper import monthly_report

from app import app, cache
from app import worker
from celery.schedules import crontab


from jinja2 import Template
import matplotlib.pyplot as plt
from base64 import b64encode
from weasyprint import HTML


# from celery_job_demo import celery
celery = worker.celery
#for csv file
import csv


@celery.task()
def just_say_hello(name):
    print("INSIDE TASK")
    print('Hello {}'.format(name))

@celery.task()
def daily_reminders():
		'''
		This will retrive all user and send reminder for their logins
		'''
		list_users = user_manager.get_all_user_last_login_time()
		cur_time = datetime.now()

		yesterday = datetime.now() - timedelta(days=1)
		for user in list_users:
			# create_user_csv_file(user.user_id)
			last_login_time = user.last_login_time
			if last_login_time < yesterday:
				user_container = create_user_container(user.user_id)
				msg = '''
				Dear {},<br>
				You have not visited Your account since one day,<br>
				Plase, Visit check the recent updates <br>
				<br>
				Thank you<br>
				Blog Lite Team
				'''.format(user_container.name)
				send_email(to=user.user_id, subject="Daily Reminder", msg=msg)

def create_monthly_report_html_helper(user:tuple)->str:
		print(user)
		user_id = user.user_id
		user_name = user.fname + " " + user.lname
		list_final_post, total_likes, total_comments, total_post_count = monthly_report(user_id)
		template_file = open("celery_jobs/monthly_report.html")
		TEMPLATE = template_file.read()
		template_file.close()
		template = Template(TEMPLATE)
		image_labels  = ['Number of Posts', 'Liker', 'Comments']
		image_data=[total_post_count, total_likes, total_comments]
		image_name = "barchart.png"
		plt.bar(image_labels, height=image_data, color=['blue', 'red', 'green'])
		plt.ylabel(image_name)
		plt.savefig("barchart.png")
		with open(image_name, "rb") as image_file:
			image_data = image_file.read()
		image_base64 = b64encode(image_data)
		message= template.render(user_name = user_name, total_post_count = total_post_count, total_likes=total_likes, total_comments=total_comments, image_base64=image_base64)
		return message

@celery.task()
def create_pdf_from_html(user_id:str, template:HTML):
	''' create pdf from html'''
	file_name = str(user_id) + ".pdf"
	path = os.path.join(os.curdir , 'static', 'download', file_name)
	print('final save path is', path)
	if os.path.exists(path):
		os.remove(path)
	
	template.write_pdf(target=file_name)
	return file_name


#########################################################################

@celery.task()
def monthly_html_report():
	''' This will send monthly project report '''
	list_users = user_manager.get_all_uesr()
	print(list_users)
	for user in list_users:
		message = create_monthly_report_html_helper(user)
		print('html report ready')
		# print(message)
		print ('monthly html report ready')
		file_name = user.user_id + '.html'
		file_path = os.path.join(os.curdir, 'static', 'download', file_name)
		html_f = open(file_path, 'w')
		html_f.writelines(message)
		send_email(to=user.user_id, subject='Monthly Html report', msg=message, attachment=file_path)

##########################################################################

@celery.task()
def monthly_pdf_report():
	list_users =user_manager.get_all_uesr()
	for user in list_users:
		try:
			message = create_monthly_report_html_helper(user)
			print('html report ready')
			html = HTML(string=message)
			file_name = create_pdf_from_html(user.user_id, html)
			send_email(user.user_id, "Monthly pdf report", msg=message, attachment=file_name)
			print ('monthly pdf report ready')
		except Exception as e:
			print('exception arrived in pdf gen', e)




# from flask_restful import Resource
# from Api.misc_utils import create_response

# class ExportApi(Resource):
# 	def get(self, user_id):
# 		create_user_csv_file.delay(user_id)
# 		return create_response({}, 200)
# 	def options(self, user_id):
# 		return create_response({}, 200)
# # from app import api
# # api.add_resource(ExportApi, '/api/v2/ex/test')

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
	# sender.add_periodic_task(1.0, just_say_hello.s('hi'), name='kuch bhi')
	# sender.add_periodic_task(crontab(minute=28, hour=23), daily_reminders.s(), name='daily_reminders')
	# sender.add_periodic_task(30, daily_reminders.s(), name='daily_reminders')
	sender.add_periodic_task(crontab(minute=15, hour=7), daily_reminders.s(), name='daily_reminders')

	print('changed')
	sender.add_periodic_task(crontab(minute=00, hour=7), monthly_html_report.s(), name='monthly_html_repost')
	sender.add_periodic_task(crontab(minute=00, hous=2), monthly_pdf_report.s(), name='monthly_pdf_report')
	# #testing 
	# sender.add_periodic_task(20, monthly_html_report.s(), name='monthly_html_repost')
	# sender.add_periodic_task(20, monthly_pdf_report.s(), name='monthly_pdf_report')

