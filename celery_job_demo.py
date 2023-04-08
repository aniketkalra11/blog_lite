import worker
from datetime import datetime
from controller.user_controller import *
from controller.post_controller import *
import csv
from mail_config import send_email
celery = worker.celery

@celery.task()
def just_say_hello(name:str):
    print('inside celery task')


@celery.task()
def create_user_csv_file(user_id:str):
	''' return csv file on demand '''
	csv_filds = ['user_name', 'Post_title', 'Post_containt', 'timestamp', 'image_url']
	csv_data = []
	list_posts = c_get_user_post(user_id)
	# user_conatiner = create_user_container(user_id)

	# csv_data.append(list_posts)
	for post in list_posts:
		l = [post.user_name, post.title, post.caption, post.timestamp, post.image_url]
		csv_data.append(l)

	file_name = user_id + ".csv"
	file_path = os.path.join(os.curdir, 'static', 'download', file_name)
	print(file_path)
	with open(file_path, 'w') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(csv_filds)
		csvwriter.writerows(csv_data)
	msg = '''
	Dear {}, <br>
	Please, Find attachment of  your post list <br>
	<br><br>
	Thank you
	Team Blog Lite
	'''.format(	user_manager.get_user_details(user_id).fname)
	send_email(to=user_id, subject="Custom import Job", msg=msg, attachment=file_path)