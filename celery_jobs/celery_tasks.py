from datetime import datetime, timedelta
import pytz
from controller.user_controller import *
from controller.post_controller import *
from model.misc_utils import getTodaysDate
from mail_config import send_email
from montly_jobs_helper import monthly_report

from app import app, cache
from app import worker

from celery.schedules import crontab

celery = worker.celery

from jinja2 import Template
import matplotlib.pyplot as plt
from base64 import b64encode
from weasyprint import HTML






@celery.task()
def daily_reminders():
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
				print(user_container)
				# send_email(user.user_id, '''
				# Hello {0}
				# you have been not visited for more than 1 one day please 
				# login and check the activites
			
				# Thank you for using Blog Lite Application
				# '''.format(user_container.name))

def create_monthly_report_html(user:tuple)->str:
		user_id = user.user_id
		user_name = user.name
		list_final_post, total_likes, total_comments, total_post_count = monthly_report(user_id)
		template_file = open("monthly_report.html")
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

def create_pdf_from_html(user_id:str, template:HTML):
	''' create pdf from html'''
	file_name = str(user_id) + ".pdf"
	template.write_pdf(target=file_name)


@celery.task()
def monthly_html_report():
	''' This will send monthly project report '''
	list_users = user_manager.get_all_uesr()
	
	for user in list_users:
		message = create_monthly_report_html(user)
		print('html report ready')
		print(message)
		print ('monthly html report ready')

def monthly_pdf_report():
	list_users =user_manager.get_all_uesr()
	for user in list_users:
		message = create_monthly_report_html(user)
		print('html report ready')
		print(HTML(message))
		print ('monthly pdf report ready')







@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
	sender.add_periodic_task(crontab(minute=0, hour=23), daily_reminders.s(), name='daily_reminders')

	sender.add_periodic_task(crontab(minute=1), monthly_html_report.s(), name='monthly_report')

	sender.add_periodic_task(crontab(minute=1), monthly_pdf_report.s(), name='monthly_report')
	

