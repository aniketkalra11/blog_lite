from flask_restful import Resource
from flask_restful import fields, marshal_with, reqparse
from flask import request
from flask import Response, make_response

from controller.user_behaviour_controller import c_user_token_verification
from controller.post_controller import create_post_container_obj, UserFeedPostContainer
#!TODO: Add validation in the 
# from app import session #? Do we really require this

# from model.post_model_controller import PostModelManager
from model.common_model_object import p_m_m

# p_m_m = PostModelManager() #? Check wheather i can create shared object or not
# print('session receiving as:', session)

from .misc_utils import *

create_parser = reqparse.RequestParser()

create_parser.add_argument('user_id')
create_parser.add_argument('post_id')
create_parser.add_argument('comment_id')
create_parser.add_argument('liker_id')
create_parser.add_argument('flager_id')

liker_FB = {
    'likes' : fields.Integer
}

flager_FB = {
    'flags' : fields.Integer
}

comment_CB = {
    'total_comments': fields.Integer
}

class PostLikeApi(Resource):
    def get_num_likes(self, post_id):
        d = {}
        print('num of likes is', p_m_m.get_num_likes(post_id))
        d['likes'] = p_m_m.get_num_likes(post_id)
        return d
    @marshal_with(liker_FB)
    def get(self, liker_id, post_id):
        try:
            if p_m_m.is_user_already_flaged(liker_id, post_id):
                return 'Unable to like a page which you already flagged', 403
            p_m_m.add_like(post_id, liker_id)
        except Exception as e:
            print('exception arrived during like deleteion r', e)
            return 'error', 500
            # pass  # TODO: Raise valid http excpiton
        else:
            return self.get_num_likes(post_id), 201
        
    @marshal_with(liker_FB)
    def put(self, liker_id, post_id):
        liker_id
        data = request.data
        print(data)
        try:
            return self.get_num_likes(post_id), 201
        except Exception as e:
            print('unable to retrive the number of likes of user')
            return {'likes': 0}, 500

        

    @marshal_with(liker_FB)
    def delete(self, liker_id, post_id):
        try:
            print('receving remove like request:', liker_id)
            p_m_m.remove_like(post_id, liker_id)
        except Exception as e:
            print('exception 3 arrived during like deleteion r', e)
            return 'error', 500
            #TODO: print a valid exceptionS
        else:
            return self.get_num_likes(post_id), 201

class PostFlagApi(Resource):

    def get_num_of_flags(self, post_id):
        d = {}
        d['flags'] = p_m_m.get_num_flags(post_id)
        return d


    @marshal_with(flager_FB)
    def get(self, flager_id, post_id):
        try:
            if p_m_m.is_user_already_liked(flager_id, post_id):
                return 'Unable to like a page which you already liked', 403
            p_m_m.add_flag(post_id, flager_id)
        except Exception as e:
            print('exception 34 arrived during flag insertion r', e)
            return 'error', 500
        else:
            return self.get_num_of_flags(post_id), 201

    @marshal_with(flager_FB)
    def delete(self, flager_id, post_id):
        try:
            p_m_m.remove_flag(post_id, flager_id)
        except Exception as e:
            print('exception 324 arrived during flag deleteion r', e)
            return 'error', 500
        else:
            return self.get_num_of_flags(post_id), 201                

post_details = {
    'user_id': fields.String,
    'post_id': fields.String,
    'title': fields.String,
    'caption': fields.String,
    'timestamp': fields.DateTime,
    'image_url': fields.String
}
details = {
    'is_success': fields.Boolean,
    'post_id': fields.String
}
#! Depricated 
class PostCRUDApi(Resource):
    @marshal_with(post_details)
    def get(self, user_id, post_id):

        try:
            p_id = p_m_m.get_post_id_tuple(post_id)
            if p_id.user_id != user_id:
                return '', 404
            p = p_m_m.get_post_content(post_id)
            print(p)
            d = {
                'user_id': user_id,
                'post_id': p.post_id,
                'title': p.title,
                'caption': p.caption,
                'timestamp': p.timestamp,
                'image_url': p.image_url
            }
        except Exception as e:
            print('error arrived', e)
            return '', 404
        return d, 200
    @marshal_with(details)
    def delete(self, user_id, post_id):
        print('deleteing post ', post_id)
        p = p_m_m.get_post_id_tuple(post_id)
        try:
            if p.user_id != user_id:
                return 'no allowed', 403
            try:
                p_m_m.remove_post(user_id, post_id)
            except Exception as e:
                return 'no allowed', 403
        except: 
            return {'is_success': False, 'post_id': post_id}, 404
        d = {
            'is_success': True,
            'post_id': post_id
        }
        print('post removed')
        return d, 202
    

class PostFetchApi(Resource):
    def create_post_dict(self, post_container:UserFeedPostContainer, is_detailed_required:bool) -> dict:
        d = {
            'post_id': post_container.post_id,
            'title' : post_container.title,
            'containt' : post_container.caption,
            'img_url': post_container.image_url,
            'time_stamp' : post_container.timestamp,
            'no_likes' : post_container.likes,
            'no_of_comments' : post_container.comment_count,
            'is_user_already_liked' : post_container.is_already_liked,
            'err': ""
        }
        return d
    # @marshal_with(post_container)
    def post(self):
        form = request.get_json()
        user_id = form.get('user_id')
        token = form.get('token')
        post_id = form.get('post_id')
        is_detailed_required = form.get('detail_required')
        # result, err = c_user_token_verification(user_id, token)
        result = True
        if result:
            post_container = create_post_container_obj(user_id, post_id, is_detailed_required)
            if post_container:
                d = self.create_post_dict(post_container, is_detailed_required)
                return create_response(d, 200, PostApiResponse.post_container)
            err = "no container found"
            return create_response({'is_success': False,'err': err}, 500, UserApiResponse.user_operation)
        return create_response({'is_success': False,'err': err}, 500, UserApiResponse.user_operation)

    def options(self):
        return create_response({}, 200)



class PostApiV2(Resource):
    '''
        This class is responsible for fetching post, creating post, and deleting an
        existing post.
        This will provide post as prescribed format defined in *post_container* dict
    '''
    def print_details(self, u_id, post_id, operation):
        print("PostApiV2: ", operation, " request received for user_id: ", u_id, " on post_id: ", post_id)


    def get(self, user_id, post_id):
        ''' This will provide post details on given post id,
            Token will be verified in case of private post, 
            For performance reasons we are ignoring token checks for public posts
        '''
        self.print_details(user_id, post_id, OperationStrings.combine(OperationStrings.POST, OperationStrings.FETCH))
        ''' already did in post fetch api '''
        post_container = post_container = create_post_container_obj(user_id, post_id, False)
        if post_container:
            return create_response(post_container, 200, PostApiResponse.post_container)
        else:
            return create_response({}, 500)
        
    
    def post(self, user_id, post_id=""):
        ''' this is responsible for post_id creation and making entry in database '''
        self.print_details(user_id, post_id, OperationStrings.combine(OperationStrings.POST, OperationStrings.CREATE))
        print(request.files)
        return create_response({}, 200, PostApiResponse.post_container)


    def delete(self, user_id, post_id):
        ''' this is responsible for post to delete from the database and provide proper response in this regard '''
        self.print_details(user_id, post_id, OperationStrings.combine(OperationStrings.POST, OperationStrings.DELETE))
        pass

    def options(self, user_id, post_id):
        print('option receiving')
        d = {}
        return create_response({}, 200)





class PostLikeApiV2(Resource):
    '''
        This class is responsible for post like operations 
        Post like operations are :
        1. get list of likers
        2. like given post
        3. remove like from given post 
        ***TOKEN verification is mendatory for these classes
    '''

    def print_details(self, user_id, post_id, operation):
        print("PostLikeApiV2 ", operation, " request received for user_id: ", user_id , " on post_id: ", post_id)
    # @marshal_with(post_like_details)
    def get(self, user_id, post_id):
        ''' This will return number of likes and list of likers '''
        self.print_details(user_id, post_id, OperationStrings.combine(OperationStrings.POST, OperationStrings.FETCH))
        post_container = create_post_container_obj(user_id, post_id=post_id, is_detailed_required= True)
        if post_container:
            return create_response(post_container, 200, PostApiResponse.post_like_details)
        else:
            return ({}, 500)

    # @marshal_with(post_like_operation)
    def put(self, user_id, post_id):
        ''' This will add like in give list '''
        self.print_details(user_id, post_id, OperationStrings.combine(OperationStrings.ADD, OperationStrings.LIKE))
        pass

    # @marshal_with(post_like_operation)
    def delete(self, user_id, post_id):
        ''' This will remove post in given list '''
        self.print_details(user_id, post_id, OperationStrings.combine(OperationStrings.DELETE, OperationStrings.LIKE))
        pass


class PostCommentApiV2(Resource):
    ''' This will provide post comment details '''
    def get(self, user_id, post_id):
        print('Post comment Api', user_id, ' post_id:', post_id)
        post_container = create_post_container_obj(user_id, post_id, True)
        if post_container:
            print(post_container.comments)
        return create_response(post_container, 200, PostApiResponse.post_comments_list)
