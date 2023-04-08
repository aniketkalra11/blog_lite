import os
from datetime import datetime
# from model.post_model_controller import PostModelManager
from model.common_model_object import p_m_m
from markupsafe import Markup
from .user_controller import get_user_name
from .common_function import *

# p_m_m = PostModelManager()
print('creating post model')
'''
Post Mostly edited via api so most of the stuff will exists in Api folder
'''

class PostCommentContainer:
	def __init__(self, comment_id):
		#print('post comment id:', comment_id)
		self.comment = p_m_m.get_comment_from_comment_id(comment_id)
		if self.comment:
			self.commenter_name = get_user_name(self.comment.commenter_id)
			#print('commenter name received as:', self.commenter_name)
			self.comment_content = self.comment.comment_content
			self.commenter_id = self.comment.commenter_id
		else:
			raise Exception('No comment Found')
	def __str__(self):
		return str(self.comment) + " " + str(self.commenter_name) + " " + str(self.commenter_id)
	
class PostLikeContainer:
	def __init__(self, post_like_tuple):
		# print("Post like creation: ", post_like_tuple)
		self.post_id = ''
		self.liker_id = ''
		self.time_stamp = ''
		self.liker_name = ''
		self.time_stamp = datetime.now()
		if post_like_tuple:
			self.liker_name = get_user_name(post_like_tuple.liker_id)
			self.time_stamp = post_like_tuple.time_stamp
			self.liker_id = post_like_tuple.liker_id
		else:
			print('unable to detect like details')
	
	def __str__(self):
		return self.liker_name + " " + self.liker_id + " " 
class UserFeedPostContainer:
	def __init__(self, post_id, is_depth_post_reqired = True):
		sql_post_data = p_m_m.get_post_content(post_id)
		#print('UserFeedContainer',sql_post_data)
		self.post_id = sql_post_data.post_id
		self.title = sql_post_data.title
		s_t = Markup.escape(sql_post_data.caption)
		#print(s_t)
		self.caption = sql_post_data.caption
		# self.caption = str(s_t)
		self.time_stamp_dt = sql_post_data.timestamp
		# print(self.time_stamp_dt)
		self.timestamp = sql_post_data.timestamp.strftime("%b %d, %Y %I:%M %p")
		# print('type of time stamp', type(self.timestamp))
		
		self.image_url = str(sql_post_data.image_url)
		#print(self.image_url)
		sql_post_id = p_m_m.get_post_id_tuple(post_id)
		#print('UserFeedContainer',sql_post_id)
		self.user_id = sql_post_id.user_id
		self.user_name = get_user_name(self.user_id)
		self.post_type = sql_post_id.post_type
		# print('post type is:', self.post_type)
		sql_post_interaction = p_m_m.get_post_interaction(post_id)
		#print('UserFeedContainer',sql_post_interaction)
		self.likes = sql_post_interaction.likes
		self.flags = sql_post_interaction.flags
		self.comment_count = sql_post_interaction.comments
		self.post_comment_id = sql_post_interaction.post_comment_id
		self.comments = []
		self.list_user_likes = []
		if is_depth_post_reqired:
			self.comments = self.get_post_comment_container(self.post_comment_id)
			self.list_user_likes = self.get_post_like_container(self.post_id)
			# print(self.list_user_likes)
		#print('UserFeedContainer',self.comments)
		#print(*self.comments)
		self.is_already_liked = False # will update later
		self.is_already_flagged = False # will update later
		self.is_already_bookmarked = False
		#print('UserFeedPostContainer construction complete')

	def get_post_comment_container(self, post_comment_id):
		#print('post_comment id is:', post_comment_id)
		comments = p_m_m.get_comments_from_post_id(post_comment_id)
		l_container = []
		for c in comments:
			try:
				con = PostCommentContainer(c.comment_id)
				l_container.append(con)
			except Exception as e:
				pass
				# print(e)
		return l_container


	def get_post_like_container(self, post_id:str)->list:
		l_likes = p_m_m.get_like_user_list(post_id)
		# print("list of likes ", l_likes)
		if not l_likes:
			return
		like_container = []
		for l in l_likes:
			# print(l)
			like_container.append(PostLikeContainer(l))
		return like_container

	def __str__(self):
		s = self.user_id +" " + self.post_id + " " + self.title + " " + self.image_url + "\n"
		return s
	
	def __eq__(self, a):
		return True if self.time_stamp_dt == a.time_stamp_dt else False
	
	def __gt__(self, a):
		return True if self.time_stamp_dt > a.time_stamp_dt else False

	def __lt__(self, a):
		return True if self.time_stamp_dt < a.time_stamp_dt else False
	
	def __ge__(self, a):
		return True if self.time_stamp_dt >= a.time_stamp_dt else False
	
	def __le__(self, a):
		return True if self.time_stamp_dt <= a.time_stamp_dt else False
	#implemented for sorting implementation



cwd = os.getcwd()
UPLOAD_FOLDER = os.path.join(cwd, 'static', 'resources', 'img')
#print(UPLOAD_FOLDER)
if not os.path.exists(UPLOAD_FOLDER):
	try:
		os.mkdir(UPLOAD_FOLDER)
	except Exception as e:
		pass
#print(UPLOAD_FOLDER)



def c_create_post(user_id:str, form_data:dict, file = None) ->list:
	debug_print('crating_post')
	debug_print('form_received as:' + str(form_data))
	title = form_data['title']
	caption = form_data['caption']
	post_type = None
	try:
		post_type = form_data['type']
	except Exception as e:
		print('e: ', e)
		print('skipping type of post')
	#print('title as ', title, 'caption as:', caption)
	# file = form_data.files['image']
	filedir = None
	file_name = None
	if file and file.filename != '' :
		if allowed_file(file.filename):
			file_name = create_file_name(user_id, file.filename)
			#print(file_name, 'created')
			filedir = os.path.join(UPLOAD_FOLDER, file_name)
			debug_print('file dir is:' + str(filedir))
		else:
			return False, "Improper file format received"
	else:
		print('no file detected continuing')

	is_sucess = p_m_m.add_post(user_id, title=title, caption= caption, imageurl= file_name, post_type= post_type)
	if is_sucess:
		if file_name:
			file.save(filedir)
			#print('images saved')
	else:
		return False, 'Database entry failed'
	# #print('file receiving as:',file)
	return True, 'Success'

def c_add_comment(user_id:str, post_id:str, comment_content:str)->list:
	debug_print('Adding a new comment to list')
	try:
		is_suc, reason = p_m_m.add_comment(post_id, user_id, comment_content)
	except Exception as e:
		is_suc = False
		#print('exception arrived', e)
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
	#print(r_p)
	r_p.sort(reverse=True)
	return r_p
def c_update_user_like_dislike_flags(user_id:str, posts:list) -> list:
	for p in posts:
		p.is_already_liked = p_m_m.is_user_already_liked(user_id, p.post_id)
		p.is_already_flagged = p_m_m.is_user_already_flaged(user_id, p.post_id)
		p.is_already_bookmarked = p_m_m.is_user_already_bookmarked(user_id, p.post_id)
	return posts

def c_get_home_page_post(user_id:str, user_following_list:list):
	# debug_print('searching following list for user:'+ user_id)
	# debug_print('following list received as:' + str(user_following_list))
	list_posts = []
	for user in user_following_list:
		try:
			posts = c_get_user_post(user.following_id)
		except Exception as e:
			#print('exception arrived for user_id: ', user_id, ' exception:', str(e))
			posts = c_get_user_post(user.user_id)

		posts = c_update_user_like_dislike_flags(user_id, posts)
		list_posts.extend(posts)
	list_posts.sort(reverse= True)
	#print(list_posts)
	return list_posts
def remove_image(img_url):
	file_dir = os.path.join(UPLOAD_FOLDER, img_url) 
	if os.path.isfile(file_dir):
		#print('removing old photo')
		os.remove(file_dir)
	else:
		print('unable to remove image')

def c_edit_post(user_id:str, post_id:str, form_data, file= None)->list:
	debug_print('update post request received for')
	warn_str = ''
	old_post = c_get_post_by_post_id(post_id)
	try:
		title = form_data['title']
		caption = form_data['caption']
		photo_d = form_data['photo_d']
		post_type = None
		try:
			post_type = form_data['type']
		except:
			pass
		img_url = ''
		if file == None:
			img_url = 'NOT_AVAILABLE' if photo_d == 'remove_photo' else None
		else:
			img_url = file.filename
			if allowed_file(img_url):
				warn_str = 'updating photo'
				img_url = create_file_name(user_id, file.filename)
			else:
				return False, 'Unknown File received'
		p_m_m.edit_post(post_id, title, caption, img_url, post_type)
	except Exception as e:
		debug_print('Exception arrived during post edit' + str(e))
		warn_str = 'Unable to edit post' + str(e)
		return False, warn_str
	else:
		if img_url:
			if old_post.image_url != img_url or (img_url and img_url == 'NOT_AVAILABLE'):
				# old_img_dir = os.path.join(UPLOAD_FOLDER, old_post.image_url)
				# debug_print(old_img_dir)
				remove_image(old_post.image_url)
			if img_url != '' and img_url != "NOT_AVAILABLE":
				fildir = os.path.join(UPLOAD_FOLDER, img_url)
				debug_print("saving new file" + fildir)
				file.save(fildir)
		return True, warn_str

def create_post_container_obj(user_id, post_id, is_detailed_required = True) -> UserFeedPostContainer:
	obj = None
	if len(post_id) > 4:
		try:
			obj = UserFeedPostContainer(post_id, is_detailed_required)
		except Exception as e:
			debug_print('Unable to create post object for ' + str(post_id))
			print(e)
		else:
			obj.is_already_flagged = p_m_m.is_user_already_flaged(user_id, post_id)
			obj.is_already_liked = p_m_m.is_user_already_liked(user_id, post_id)
			obj.is_already_bookmarked = p_m_m.is_user_already_bookmarked(user_id, post_id)
	return obj

def c_get_post_by_post_id(post_id:str)->UserFeedPostContainer:
	obj = UserFeedPostContainer(post_id)
	return obj

def c_delete_post(user_id, post_id)-> list:
	debug_print('delete post:'+ post_id)
	old_post = c_get_post_by_post_id(post_id)
	try:
		p_m_m.remove_post(user_id, post_id)
	except Exception as e:
		print('unable to delete post')
		return False, str(e)
	else:
		remove_image(old_post.image_url)
		print('image removed')
		return True, ''

def c_add_bookmark(user_id:str, post_id:str)->list:
	''' This will add bookmark to table '''
	try:
		if not p_m_m.is_user_already_bookmarked(user_id, post_id):
			p_m_m.add_bookmark(user_id, post_id)
		return True , ''
	except Exception as e:
		debug_print("unable to add bookmar", e)
		return False, 'Database entry failed'

def c_remove_bookmark(user_id:str, post_id:str) ->list:
	''' This will remove bookmark '''
	try:
		if p_m_m.is_user_already_bookmarked(user_id, post_id):
			p_m_m.remove_bookmark(user_id, post_id)
		return True , ''
	except Exception as e:
		debug_print("unable to add bookmar", e)
		return False, 'Database entry failed'

def c_get_user_bookmark_post(user_id:str)->list:
	list_raw_post = p_m_m.get_post_bookmark_list_by_user_id(user_id)
	list_post_container = []
	for x in list_raw_post:
		temp_container = create_post_container_obj(user_id, x.post_id)
		list_post_container.append(temp_container)
	return list_post_container

def debug_print(s:str):
    print('post_controller:', s)