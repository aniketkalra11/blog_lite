from flask_restful import Resource
# from celery_tasks import start_export_task
from celery_job_demo import create_user_csv_file
from .misc_utils import create_response
from .misc_utils import PostApiResponse
from mail_config import send_email

class ExportApi(Resource):
	def get(self, user_id):
			''' starting new export job '''
			print('creating new async jobs')
			job_id = create_user_csv_file.delay(user_id)
			print(job_id)
			# t = start_export_task(user_id)
			d = {'is_success': True, 'err': ''}
			return create_response(d, 200, PostApiResponse.post_operation_result)
	
	def options(self, user_id):
		return create_response({}, 200)

