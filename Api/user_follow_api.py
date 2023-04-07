from flask_restful import Resource
from flask_restful import fields, marshal_with, reqparse
#!TODO: Add validation in the 
from flask import request
from model.common_model_object import user_manager
from .misc_utils import *
from controller.user_controller import *
# user_manager = UserModelManager()


create_parser = reqparse.RequestParser()

create_parser.add_argument('user_id')
create_parser.add_argument('f_user_id')

follower_count = {
    'num_followers': fields.Integer,
    'num_of_following': fields.Integer
}

class FollowApi(Resource):
    @marshal_with(follower_count)
    def post(self, user_id, f_user_id):
        try:
            user_manager.add_user_follower(f_user_id, user_id)
            user_manager.add_user_following(user_id, f_user_id)
        except Exception as e:
            print('exception arrived during like deleteion r', e)
            return create_response({}, 500)
            # pass  # TODO: Raise valid http excpiton

        t = user_manager.get_user_post_flr_flwing_count(f_user_id)
        print('API count rec', t)
        d ={'num_followers': t[0], 'num_of_following': t[1]}
        res_receive = create_response(d, 200, UserApiResponse.follower_count)
        print(res_receive.headers)
        return res_receive

    @marshal_with(follower_count)
    def delete(self, user_id, f_user_id):
        try:
            user_manager.remove_user_follower(f_user_id, user_id)
            user_manager.remove_user_following(user_id, f_user_id)
        except Exception as e:
            print('exception arrived during like deleteion r', e)
            return create_response(d, 500)
            # pass  # TODO: Raise valid http excpiton

        t = user_manager.get_user_post_flr_flwing_count(f_user_id)
        print('API count rec', t)
        d ={'num_followers': t[0], 'num_of_following': t[1]}
        final_res = create_response(d, 200, UserApiResponse.follower_count)
        print('final response for api', final_res.headers)
        return final_res
    def options(self, user_id, f_user_id):
        return create_response({}, 200)
    

class FollowUserApi2(Resource):
    ''' This api is responsible for creating a follow user and following of a user '''
    def put(self):
        ''' adding a new user'''
        try:
            print('header of request', request.headers)
            json = request.get_json()
            f_user_id = json['f_user_id']
            user_id = json['user_id']
            user_manager.add_user_follower(f_user_id, user_id)
            user_manager.add_user_following(user_id, f_user_id)
        except Exception as e:
            print('exeception arrived during follow creation', e)
            return create_response({}, 500)
        t = user_manager.get_user_post_flr_flwing_count(f_user_id)
        print('API count rec', t)
        d ={'num_followers': t[0], 'num_of_following': t[1]}
        return create_response(d, 200, UserApiResponse.follower_count)
    def post(self):
        try:
            print(request.headers)
            json = request.get_json()
            f_user_id = json['f_user_id']
            user_id = json['user_id']
            user_manager.remove_user_follower(f_user_id, user_id)
            user_manager.remove_user_following(user_id, f_user_id)
        except Exception as e:
            print('exception arrived during like deleteion r', e)
            return create_response({}, 500)
        
        t = user_manager.get_user_post_flr_flwing_count(f_user_id)
        print('API count rec', t)
        d ={'num_followers': t[0], 'num_of_following': t[1]}
        final_res = create_response(d, 200, UserApiResponse.follower_count)
        print('final response for api', final_res.headers)
        return final_res

    def options(self):
        return create_response({}, 200)
    

class GetUserFollowingList(Resource):
    '''
        This will return user following list
    '''
    def get(self, user_id):
        '''return list ids'''
        list_following = c_get_user_following_list(user_id)
        d = {'user_id' : user_id, 'list_user_container': list_following}
        return create_response(d, 200, UserApiResponse.user_search_result)


    def options(self, user_id):
        return create_response({}, 200)


class GetUserFollowerList(Resource):
    '''
    This will return user follower list
    '''
    def get(self, user_id):
        '''return list ids'''
        list_follower = c_get_user_follower_list(user_id)
        d = {'user_id' : user_id, 'list_user_container': list_follower}
        return create_response(d, 200, UserApiResponse.user_search_result)


    def options(self, user_id):
        return create_response({}, 200)