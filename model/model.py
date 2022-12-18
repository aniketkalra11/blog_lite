from database.database import db

NOT_AVAILABLE = "NOT_AVAILABLE"
USER = "USER"
ADMIN = "ADMIN"
#* Adding one to many relation
class UserIdPassword(db.Model):
	__tablename__ = 'user_id_password'
	seq_no = db.Column(db.Integer, autoincrement=True)
	user_id = db.Column(db.String, primary_key = True)
	password = db.Column(db.String, nullable= False)
	# user_details = db.relationship('UserDetails', foreign_key = ['user_details.user_id'], backref='user_id_password', lazy=True)
	user_details = db.relationship('UserDetails', backref='user_id_password', cascade="all, delete-orphan", lazy=True)


class UserDetails(db.Model):
	__tablename__ = "user_details"
	user_id = db.Column(db.String,  db.ForeignKey('user_id_password.user_id'), nullable= False, primary_key = True)
	fname = db.Column(db.String, nullable= False)
	lname = db.Column(db.String, nullable = False, default= NOT_AVAILABLE)
	dob = db.Column(db.DateTime, nullable = False)
	#Address starting
	city = db.Column(db.String, nullable = False)
	profession = db.Column(db.String, nullable = False, default= NOT_AVAILABLE)
	member_type = db.Column(db.String, nullable= False, default = USER) # need to add attional constains on this
	#currently there are two type of user only 1. admin and 2. user

class UserPostAndFollowerInfo(db.Model):
	__tablename__ = 'user_post_and_follower_info'
	# total_count = db.Column(db.Integer, autoincrement=True)
	user_id = db.Column(db.String, db.ForeignKey('user_id_password.user_id'), nullable= False, primary_key= True)
	num_followers = db.Column(db.Integer, default= 0)
	num_of_following = db.Column(db.Integer, default= 0)
	num_of_post = db.Column(db.Integer, default= 0)

class UserFollowers(db.Model):
	__tablename__ = 'user_followers'
	int_count = db.Column(db.Integer, autoincrement=True, primary_key= True) # for error resolution
	user_id = db.Column(db.String, db.ForeignKey('user_id_password.user_id'), nullable= False)
	follower_id = db.Column(db.String, db.ForeignKey('user_id_password.user_id'), nullable= False)

class UserFollowing(db.Model):
	__tablename__ = 'user_following'
	int_count = db.Column(db.Integer, autoincrement=True, primary_key= True) # for error resolution
	user_id = db.Column(db.String, db.ForeignKey('user_id_password.user_id'), nullable= False)
	following_id = db.Column(db.String, db.ForeignKey('user_id_password.user_id'), nullable= False)

#Stating Post content


class PostId(db.Model):
	__tablename__ = 'post_id'
	# int_count = db.Column(db.Integer, autoincrement=True, primary_key= True) # for error resolution
	user_id = db.Column(db.String, db.ForeignKey('user_id_password.user_id'), nullable= False, primary_key= True)
	post_id = db.Column(db.String, primary_key = True)
	post_content = db.relationship('PostContent', backref='post_content', cascade="all, delete-orphan", lazy=True)
	post_interaction = db.relationship('PostIneraction', backref='post_interaction', cascade="all, delete-orphan", lazy= True)

class PostContent(db.Model):
	__tablename__ = "post_content"
	post_id = db.Column(db.String, db.ForeignKey('post_id.post_id'), nullable= False, primary_key= True)
	title = db.Column(db.String, nullable= False)
	caption = db.Column(db.String(1000), nullable= False, default= NOT_AVAILABLE)
	timestamp = db.Column(db.DateTime, nullable = False)
	image_url = db.Column(db.String, default=NOT_AVAILABLE) # This will store location of file in resource folder

class PostInteraction(db.Model):
	__tablename__ = "post_interaction"
	post_id = db.Column(db.String, db.ForeignKey('post_id.post_id'), nullable= False, primary_key= True)
	likes = db.Column(db.Integer, default= 0)
	flags = db.Column(db.Integer, default= 0)
	post_comment_id = db.Column(db.String, unique= True, nullable= False)
	post_commet_data = db.relationship('PostCommentTable', 'post_comments', cascade="all, delete-orphan", lazy= True)
	post_like_data = db.relationship('PostLikeTable', 'post_likes', cascade="all, delete-orphan", lazy= True)
	post_flag_data = db.relationship('PostFlagTable', 'post_flags', cascade="all, delete-orphan", lazy= True)
	# post_like_id = db.Column(db.String, unique=True, nullable= False)

class PostCommentTable(db.Model):
	__tablename__ = "post_comments"
	# comment_id = db.Column(db.Integer, primary_Key= True, autoincrement= True)
	comment_id = db.Column(db.String, primary_key= True)
	post_comment_id = db.Column(db.String, db.ForeignKey('post_interaction.post_comment_id'), nullable= False)
	commenter_id = db.Column(db.String, db.ForeignKey('user_id_password.user_id'), nullable= False)
	comment_content = db.Column(db.String(300), nullable= False)

class PostLikeTable(db.Model):
	__tablename__ = "post_likes"
	like_counter= db.Column(db.Integer, autoincrement=True, primary_key= True)
	post_id = db.Column(db.String, db.ForeignKey('post_id.post_id'), nullable= False)
	liker_id = db.Column(db.String, db.ForeignKey('user_id_password.user_id'), nullable= False)

class PostFlagTable(db.Model):
	__tablename__ = "post_flags"
	flag_counter= db.Column(db.Integer, autoincrement=True, primary_key= True)
	post_id = db.Column(db.String, db.ForeignKey('post_id.post_id'), nullable= False)
	flagger_id = db.Column(db.String, db.ForeignKey('user_id_password.user_id'), nullable= False)


def init_db():
	db.create_all()