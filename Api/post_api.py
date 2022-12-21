from flask_restful import Resource
from flask_restful import fields, marshal_with, reqparse
#!TODO: Add validation in the 
# from app import session #? Do we really require this

from model.post_model_controller import PostModelManager

p_m_m = PostModelManager() #? Check wheather i can create shared object or not
# print('session receiving as:', session)


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
    @marshal_with(liker_FB)
    def get(self, liker_id, post_id):
        try:
            p_m_m.add_like(post_id, liker_id)
        except Exception as e:
            print('APi',e)
            return 'error', 500
            # pass  # TODO: Raise valid http excpiton
        else:
            return p_m_m.get_num_likes(post_id), 201

    @marshal_with(liker_FB)
    def delete(self, liker_id, post_id):
        try:
            p_m_m.remove_like(post_id, liker_id)
        except Exception as e:
            print(e)
            return 'error', 500
            #TODO: print a valid exceptionS
        else:
            return p_m_m.get_num_likes(post_id), 201

class PostFlagApi(Resource):
    @marshal_with(flager_FB)
    def get(self, flager_id, post_id):
        try:
            p_m_m.add_flag(post_id, flager_id)
        except Exception as e:
            print('Api', e)
            return 'error', 500
        else:
            return p_m_m.get_num_flags(post_id), 201

    @marshal_with(flager_FB)
    def delete(self, flager_id, post_id):
        try:
            p_m_m.remove_flag(post_id, flager_id)
        except Exception as e:
            print('Api', e)
            return 'error', 500
        else:
            return p_m_m.get_num_flags(post_id), 201                
        