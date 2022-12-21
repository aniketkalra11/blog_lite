import os
from datetime import datetime
from model.post_model_controller import PostModelManager

p_m_m = PostModelManager()
print('creating post model')
'''
Post Mostly edited via api so most of the stuff will exists in Api folder
'''
cwd = os.getcwd()
UPLOAD_FOLDER = os.path.join(cwd, 'resource')
print(UPLOAD_FOLDER)
if not os.path.exists(UPLOAD_FOLDER):
    print('creating folder')
    os.mkdir(UPLOAD_FOLDER)
print(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS= {'png', 'jpg', 'jpeg', 'gif'} #TODO: will add later
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_extension(file_name):
    return file_name.split('.')[-1]


def c_create_post(user_id:str, form_data:dict, file) ->list:
    debug_print('crating_post')
    debug_print('form_received as:' + str(form_data))
    title = form_data['title']
    caption = form_data['caption']
    print('title as ', title, 'caption as:', caption)
    # file = form_data.files['image']
    filedir = None
    if file.filename != '' and allowed_file(file.filename):
        file_name = 'user_id_' + datetime.now().strftime('%H_%M_%S') + '.' +   get_extension(file.filename)
        print(file_name, 'created')
        filedir = os.path.join(UPLOAD_FOLDER, file_name)
        debug_print('file dir is:' + str(filedir))
        # 

    is_sucess = p_m_m.add_post(user_id, title=title, caption= caption, imageurl= filedir)
    if is_sucess:
        file.save(filedir)
        print('images saved')
    else:
        return False, 'Database entry failed'
    # print('file receiving as:',file)
    return True, 'Success'
    




def debug_print(s:str):
    print('post_controller:', s)