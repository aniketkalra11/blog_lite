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
        self.debug = ''

    def create_post_id(self, user_id:str) -> str:
        # t_date = date.today()
        t_date = datetime.now()
        day = t_date.date
        #print(type(day))
        month = t_date.month
        #print(month)
        year = t_date.year #?: we will check wheather it is required or not
        time = t_date.strftime('%H_%M_%S')
        id = user_id +  "_" + time
        #print('final id is:', id)
        return id
    def create_post_comment_id(self, post_id:str)->str:
        t_date = datetime.now()
        day = str(t_date.date)
        month = str(t_date.month)
        year = t_date.year #?: we will check wheather it is required or not
        time = t_date.strftime('%H_%M_%S')
        id = post_id + "_" + time
        #print('final id is:', id)
        return id

    def create_comment_id(self, post_id, commenter_id)->str:
        t_date = datetime.now()
        id = post_id + '_' + commenter_id + '_' + t_date.strftime('%H_%M_%S')
        return id
        

    def add_post(self, user_id, title, caption = None, timestamp= datetime.now(), imageurl = None) ->bool:
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
        post_content_obj.timestamp = datetime.now()
        if imageurl:
            post_content_obj.image_url = imageurl
        post_id_obj.post_content.append(post_content_obj)
        post_id_obj.post_interaction.append(post_interaction_obj)
        try:
            self.printDebug('adding post id to database')
            db.session.add(post_id_obj)
            db.session.add(user_post_info)
            self.printDebug('Database addition complete')
        except Exception as e:
            self.printDebug('database addition failed, Rollbacked')
            # self.session.rollback()
            db.session.rollback()
            return False
        else:
            #print('Commiting changes')
            db.session.commit()
            return True
    
    def add_like(self, post_id, liker_id):
        self.debug = 'getting post as:' + post_id + ', and liker_id:' + liker_id
        self.printDebug(self.debug)
        post_interaction = PostInteraction.query.filter_by(post_id = post_id).first()
        if post_interaction == None:
            self.post_content_not_found_exception(post_id)
        #already likes check 
        p_l = PostLikeTable.query.filter_by(post_id = post_id, liker_id = liker_id).first()
        if p_l != None:
            self.printDebug("Post already liked by user:" + liker_id)
            return
        like_data = PostLikeTable(post_id= post_id, liker_id= liker_id)
        post_interaction.likes = post_interaction.likes + 1
        post_interaction.post_like_data.append(like_data)
        self.add_to_db(post_interaction)
        # try:
        #     self.debug = "Adding to data base"
        #     self.printDebug(self.debug)
        #     db.session.add(post_interaction)
        #     self.debug = "Added successfully"
        # except Exception as e:
        #     self.debug = 'Exception arrived as:' + e.args
        #     print(e)
        #     self.printDebug(self.debug)
        #     db.session.rollback()
        # else:
        #     db.session.commit()
        #     print('like added successfully')

    def add_flag(self, post_id, flager_id):
        self.debug = 'getting post as:' + post_id + ', and flagger_id:' + flager_id
        self.printDebug(self.debug)
        post_interaction = PostInteraction.query.filter_by(post_id = post_id).first()
        if post_interaction == None:
            self.post_content_not_found_exception(post_id)
        p_f = PostFlagTable.query.filter_by(post_id = post_id, flagger_id = flager_id).first()
        if p_f != None:
            self.printDebug('Already flagged by user:' + flager_id)
            return
        # like_data = PostLikeTable(post_id= post_id, liker_id= liker_id)
        flag_data = PostFlagTable(post_id = post_id, flagger_id = flager_id)
        post_interaction.flags = post_interaction.flags + 1
        post_interaction.post_flag_data.append(flag_data)
        self.add_to_db(post_interaction)
        # try:
        #     self.debug = "Adding to data base"
        #     self.printDebug(self.debug)
        #     db.session.add(post_interaction)
        #     self.debug = "Added successfully"
        # except Exception as e:
        #     self.debug = 'Exception arrived as:' + e.args
        #     print(e)
        #     self.printDebug(self.debug)
        #     db.session.rollback()
        # else:
        #     db.session.commit()
        #     print('like added successfully')
    
    def add_comment(self, post_id:str, commenter_id:str, comment_content:str) ->list:
        ''''
        returing list will contain exactly two content 
        1. bool for success
        2. reason
        '''
        # comment_id = self.create_post_comment_id(post_id)
        comment_id = self.create_comment_id(post_id, commenter_id)
        self.printDebug('post comment id receiving as:' + comment_id)
        post_interaction = PostInteraction.query.filter_by(post_id = post_id).first()
        if post_interaction == None:
            self.post_content_not_found_exception(post_id)
        p_c_d = PostCommentTable(post_comment_id = post_interaction.post_comment_id, commenter_id = commenter_id, comment_content = comment_content, comment_id = comment_id)
        # post_interaction.post_comment_data.append(p_c_d)
        self.add_to_db(p_c_d)
        return True, ''
        # try:
        #     db.session.add(post_interaction)
        #     self.printDebug('Adding comment into data base')
        # except Exception as e:
        #     print('excepiton arrived during comment addition', e)
        #     db.session.rollback()
        # else:
        #     self.printDebug('Comment added successfully')
        #     # print('comment added successfully')
        #     db.session.commit()

    # addition work complete
    #*starting edit work
    #? We will check what we can edit in senario
    #! Most curcial part is removal of user from the model

    
    def edit_comment(self, comment_id, content:str)->bool:
        '''
            May be we will use it
        '''
        self.printDebug('comment id recevied for comment edit:' + comment_id)
        post_comment = PostCommentTable.query.filter_by(comment_id = comment_id).first()
        if post_comment == None:
            self.printDebug('No Post comment Found with give id')
            return False
        if len(content) > 300:
            return False
        post_comment.comment_contend = content
        self.add_to_db(post_comment)

    def edit_post(self, post_id, title, caption, image_url = None ):
        #TODO: need to decide what we need to edit in this section
        old_post = self.get_post_content(post_id)
        old_post.title = title
        old_post.caption = caption
        
        old_post.image_url = image_url if image_url else old_post.image_url
        self.add_to_db(old_post)
        self.printDebug('Under construction')
        pass
       

    #* Edit section complete adding remove section
    #* get section starting here
    def get_comments_from_post_id(self, post_comment_id:str)->list:
        self.printDebug('post id receving as: ' + post_comment_id)
        comments = PostCommentTable.query.filter_by(post_comment_id = post_comment_id).all()
        #print('comments received as:', comments)
        return (comments)

    def get_comment_from_comment_id(self, comment_id:str):
        comment = PostCommentTable.query.filter_by(comment_id = comment_id).first()
        return comment if comment else None

    def get_post_id_tuple(self, post_id):
        #print('Post id recevied as:', post_id)
        return PostId.query.filter_by(post_id= post_id).first()

    def get_post_interaction(self, post_id):
        #print('Post id recevied as:', post_id)
        return PostInteraction.query.filter_by(post_id= post_id).first()
    
    def get_post_content(self, post_id):
        #print('Post id recevied as:', post_id)
        return PostContent.query.filter_by(post_id= post_id).first()
    
    def get_user_post(self, user_id:str)->list:
        #print('getting user id:', user_id)
        posts = PostId().query.filter_by(user_id = user_id).all()
        #print('received posts for user:',user_id, "posts:", posts)
        return posts
    #* Single Word query function:
    def is_user_already_liked(self, user_id, post_id):
        p_l = PostLikeTable.query.filter_by(post_id= post_id, liker_id = user_id).first()
        #print(p_l)
        return True if p_l else False

    def is_user_already_flaged(self, user_id, post_id):
        f_l = PostFlagTable.query.filter_by(post_id= post_id, flagger_id= user_id).first()
        #print(f_l)
        return True if f_l else False

    #* Remove section starting
    def remove_like(self, post_id, liker_id):
        post_like = PostLikeTable.query.filter_by(post_id = post_id, liker_id = liker_id).first()
        post_interaction = PostInteraction.query.filter_by(post_id = post_id).first()
        if post_like == None or post_interaction == None:
            self.post_content_not_found_exception(post_id)
        post_interaction.likes = post_interaction.likes - 1
        # post_interaction.post_like_data.remove(post_like)
        self.remove_from_db(post_like)

    def remove_flag(self, post_id, flager_id):
        post_flag = PostFlagTable.query.filter_by(post_id = post_id, flagger_id = flager_id).first()
        post_interaction = PostInteraction.query.filter_by(post_id = post_id).first()
        if post_flag == None or post_interaction == None:
            self.post_content_not_found_exception(post_id)
        post_interaction.flags = post_interaction.flags - 1
        # post_interaction.post_flag_data.remove(post_flag)
        self.remove_from_db(post_flag)
    
    def remove_comment(self, post_id, comment_id):
        post_comment = PostCommentTable.query.filter_by(comment_id = comment_id).first()
        post_interaction = PostInteraction.query.filter_by(post_id = post_id).first()
        if post_comment == None or post_interaction == None:
            self.post_content_not_found_exception(post_id)
        post_interaction.post_comment_data.remove(post_comment)
        self.remove_from_db(post_interaction)
    
    def remove_post(self, user_id:str, post_id:str):
        post_id_t = PostId.query.filter_by(post_id = post_id).first()
        post_interaction = PostInteraction.query.filter_by(post_id = post_id).first()
        user_post_count = UserPostAndFollowerInfo.query.filter_by(user_id = user_id).first()
        user_post_count.num_of_post = user_post_count.num_of_post - 1
        if not post_id_t or not post_interaction:
            self.post_content_not_found_exception(post_id)
        self.remove_from_db(post_interaction)
        self.remove_from_db(post_id_t)
        self.add_to_db(user_post_count)
        self.printDebug('Post Removed')


    def add_to_db(self, item)-> bool:
        if item == None:
            raise Exception('None found')
        try:
            db.session.add(item)
            self.printDebug('adding to db')
        except Exception as e:
            #print('excepiton arrived during comment addition', e)
            db.session.rollback()
        else:
            self.printDebug('Comment added successfully')
            # #print('comment added successfully')
            db.session.commit()
    
    def remove_from_db(self, item):
        if item == None:
            raise Exception('None found')
        try:
            db.session.delete(item)
            self.printDebug('removing to db')
        except Exception as e:
            #print('excepiton arrived during comment addition', e)
            db.session.rollback()
        else:
            self.printDebug('Commit successfully')
            # #print('comment added successfully')
            db.session.commit()
    
    #* logic basically for get number of likes and dislikes
    def get_num_likes(self, post_id:str)->int:
        post_details = PostInteraction.query.filter_by(post_id = post_id).first()
        # assuming this always exists
        self.printDebug('num of likes' + str(post_details.likes))
        return post_details.likes

    def get_num_flags(self, post_id:str)->int:
        post_de = PostInteraction.query.filter_by(post_id = post_id).first()
        self.printDebug('returing num of flags:' + str(post_de.flags))
        return post_de.flags


    def post_content_not_found_exception(self, post_id):
        raise Exception('no Post exists with post id:' + post_id)


    def printDebug(self, s):
        print('PostModelManager: ', s)



