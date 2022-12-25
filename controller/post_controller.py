import os
from datetime import datetime
from model.post_model_controller import PostModelManager
from .user_controller import get_user_name

p_m_m = PostModelManager()
print('creating post model')
'''
Post Mostly edited via api so most of the stuff will exists in Api folder
'''
class UserFeedPostContainer:
	def __init__(self, post_id):
		sql_post_data = p_m_m.get_post_content(post_id)
		print('UserFeedContainer',sql_post_data)
		self.post_id = sql_post_data.post_id
		self.title = sql_post_data.title
		self.caption = sql_post_data.caption
		self.timestamp = sql_post_data.timestamp
		self.image_url = str(sql_post_data.image_url)
		print(self.image_url)
		sql_post_id = p_m_m.get_post_id_tuple(post_id)
		print('UserFeedContainer',sql_post_id)
		self.user_id = sql_post_id.user_id
		self.user_name = get_user_name(self.user_id)
		sql_post_interaction = p_m_m.get_post_interaction(post_id)
		print('UserFeedContainer',sql_post_interaction)
		self.likes = sql_post_interaction.likes
		self.flags = sql_post_interaction.flags
		self.post_comment_id = sql_post_interaction.post_comment_id
		self.comments = p_m_m.get_comments_from_post_id(self.post_comment_id)
		print('UserFeedContainer',self.comments)
		self.is_already_liked = False # will update later
		self.is_already_flagged = False # will update later
		print('UserFeedPostContainer construction complete')

	def __str__(self):
		s = self.user_id +" " + self.post_id + " " + self.title + " " + self.image_url + "\n"
		return s
	
	def __eq__(self, a):
		return True if self.timestamp == a.timestamp else False
	
	def __gt__(self, a):
		return True if self.timestamp > a.timestamp else False

	def __lt__(self, a):
		return True if self.timestamp < a.timestamp else False
	
	def __ge__(self, a):
		return True if self.timestamp >= a.timestamp else False
	
	def __le__(self, a):
		return True if self.timestamp <= a.timestamp else False
	#implemented for sorting implementation



cwd = os.getcwd()
UPLOAD_FOLDER = os.path.join(cwd, 'static', 'resources', 'img')
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

def c_add_comment(user_id:str, post_id:str, comment_content:str)->list:
	debug_print('Adding a new comment to list')
	try:
		is_suc, reason = p_m_m.add_comment(post_id, user_id, comment_content)
	except Exception as e:
		is_suc = False
		print('exception arrived', e)
		reason = str(e)
	if not is_suc:
		print('add comment_failed')
	return is_suc, reason

def c_get_user_post(user_id:str)->list:
	posts = p_m_m.get_user_post(user_id)

	r_p = []
	for p in posts:
		obj =create_post_container_obj(p.user_id, p.post_id)
		if obj:
			r_p.append(obj)
	print(r_p)
	r_p.sort(reverse=True)
	return r_p

def c_get_home_page_post(user_id:str, user_following_list:list):
	debug_print('searching following list for user:'+ user_id)
	debug_print('following list received as:' + str(user_following_list))
	list_posts = []
	for user in user_following_list:
		print('searching posts for ', user.following_id)
		posts = c_get_user_post(user.following_id)
		print(posts)
		list_posts.extend(posts)
	list_posts.sort(reverse= True)
	print(list_posts)
	return list_posts

def create_post_container_obj(user_id, post_id):
	obj = None
	if len(post_id) > 4:
		try:
			obj = UserFeedPostContainer(post_id)
		except Exception as e:
			debug_print('Unable to create post object for ' + str(post_id))
			print(e)
		else:
			obj.is_already_flagged = p_m_m.is_user_already_flaged(user_id, post_id)
			obj.is_already_liked = p_m_m.is_user_already_liked(user_id, post_id)
	return obj

def debug_print(s:str):
    print('post_controller:', s)