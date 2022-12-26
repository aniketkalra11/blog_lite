from datetime import datetime

ALLOWED_EXTENSIONS= {'png', 'jpg', 'jpeg', 'gif'} #TODO: will add later
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_extension(file_name):
    return file_name.split('.')[-1]

def create_file_name(user_id:str, filename)->str:
	return user_id + '_' + datetime.now().strftime('%H_%M_%S') + '.' +   get_extension(filename)