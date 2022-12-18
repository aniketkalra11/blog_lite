from datetime import datetime
from datetime import date
from .model import db
from .model import PostId
from .model import  UserPostAndFollowerInfo
from .model import PostLikeTable
from .model import PostCommentTable
from .model import PostContent
from .model import PostFlagTable
from .model import PostInteraction

'''
Post Id Format strategy 
1. user_id_date_time(time in the format of hr::min)
example: ani_17_12_22_00_12 will be the post id for minimal collision

'''

class PostModelManager():
    '''
        This class will contain all esential functionalities of post
    '''
    def __init__(self):
        print('Starting Post Manager')
        self.post_count = 0

    def create_post_id(self, user_id:str) -> str:
        # t_date = date.today()
        t_date = datetime.now()
        day = str(t_date.date)
        month = str(t_date.month)
        year = t_date.year #TODO: we will check wheather it is required or not
        time = t_date.strftime('%H_%M_%S')
        id = user_id + "_" + day + "_" + month + "_" + time
        print('final id is:', id)
        return id
    def create_post_comment_id(self, post_id:str)->str:
        return '123'
        

    def add_post(self, user_id, title, caption = None, timestamp= datetime.now(), imageurl = None):
        user_post_info = UserPostAndFollowerInfo.query.filter_by(user_id = user_id).first()
        if user_post_info == None:
            raise Exception('User not found in info table')
        user_post_info.num_of_post = user_post_info.num_of_post + 1
        post_id = self.create_post_id(user_id)
        post_comment_id = self.create_post_comment_id(post_id)
        # print('post_id received as:', post_id)
        self.printDebug(post_id + 'Received as')
        post_id_obj = PostId(user_id = user_id, post_id = post_id)
        post_content_obj = PostContent(post_id = post_id, title= title)
        post_interaction_obj = PostInteraction(post_id = post_id, post_comment_id = post_comment_id)
        
        if caption:
            post_content_obj.caption = caption
        post_content_obj.timestamp = timestamp
        if imageurl:
            post_content_obj = imageurl
        post_id_obj.post_content.append(post_content_obj)
        try:
            self.printDebug('adding post id to database')
            db.session.add(post_id_obj)
            db.session.add(user_post_info)
            self.printDebug('Database addition complete')
        except Exception as e:
            self.printDebug('database addition failed, Rollbacked')
            # self.session.rollback()
            db.session.rollback()
        else:
            print('Commiting changes')
            db.session.commit()


    

    def printDebug(self, s):
        print('PostModelManager: ', s)



