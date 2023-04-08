from .post_controller import *
from .user_controller import *

list_recent_posts = []
dumy_user_id = ''
def update_recent_posts(user_id:str):
		''' This will update the recent list_recent_post_ids and maintain the length 3 '''
		global list_recent_posts, dumy_user_id
		post_container = c_get_user_post(user_id)[0]
		if post_container.image_url == "NOT_AVAILABLE":
			return
		if post_container.post_type == "private":
			return
		print('updating recent post dict')
		pre_post_id = ''
		if len(list_recent_posts) >=3:
			pre_post_id = list_recent_posts.pop()
		# post_container = UserFeedPostContainer(post_id, is_depth_post_reqired= False)
		list_recent_posts.insert(0, post_container)
		# print('previous post_id is: ', pre_post_id, ' added post_id is:', post_container.post_id)


def initialize_list_recent_post():
		''' This will initialize recent post ids it will start when server start '''
		global list_recent_posts, dumy_user_id
		all_user_list = user_manager.get_all_uesr()
		temp_post = []
		for user in all_user_list:
				# print('extracting posts for user:', user.user_id)
				dumy_user_id = user.user_id
				user_posts = c_get_user_post(user.user_id)
				final_post = []
				for p in user_posts:
					if p.post_type == "private":
						continue
					if p.image_url != 'NOT_AVAILABLE':
						final_post.append(p)
				final_post.sort()
				if temp_post != []:
					temp_post += final_post
					temp_post.sort()
					if len(temp_post) > 3:
						temp_post = temp_post[len(temp_post) - 4:]
						# print('temp list post: ', temp_post)
				else:
					temp_post = final_post
		# print('length of temp_post', len(temp_post))
		if len(temp_post) >= 3:
			temp_post.sort() #Cross check for sorted one
			list_recent_posts = temp_post[len(temp_post) - 3:]
			list_recent_posts.reverse()
		else:
			list_recent_posts = []
		# print('recent posts are: ')
		# print(*list_recent_posts)


def get_latest_posts() ->list:
	''' return list of posts '''
	global list_recent_posts
	# print(list_recent_posts)
	# print(type(list_recent_posts))
	# print(type(list_recent_posts[0]))
	return list_recent_posts

