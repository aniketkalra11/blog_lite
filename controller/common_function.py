from datetime import datetime
import hashlib
ALLOWED_EXTENSIONS= {'png', 'jpg', 'jpeg', 'gif'} #TODO: will add later
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_extension(file_name):
    return file_name.split('.')[-1]

def get_hash_val(str2hash:str) -> str:
     return hashlib.md5(str2hash.encode()).hexdigest()

def create_file_name(user_id:str, filename)->str:
    id =  user_id + '_' + datetime.now().strftime('%H_%M_%S')
    hash = get_hash_val(id) +'.' +  get_extension(filename)
    return hash