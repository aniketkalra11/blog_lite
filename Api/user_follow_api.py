from flask_restful import Resource
from flask_restful import fields, marshal_with, reqparse
#!TODO: Add validation in the 

from model.user_model_controller import UserModelManager
user_manager = UserModelManager()


create_parser = reqparse.RequestParser()

create_parser.add_argument('user_id')
create_parser.add_argument('f_user_id')

follower_count = {
    'num_followers': fields.Integer,
    'num_of_following': fields.Integer
}

class FollowApi(Resource):
    @marshal_with(follower_count)
    def get(self, user_id, f_user_id):
        try:
            user_manager.add_user_follower(f_user_id, user_id)
            user_manager.add_user_following(user_id, f_user_id)
        except Exception as e:
            print('exception arrived during like deleteion r', e)
            return 'error', 500
            # pass  # TODO: Raise valid http excpiton
        else:
            t = user_manager.get_user_post_flr_flwing_count(f_user_id)
            print('API count rec', t)
            d ={'num_followers': t[0], 'num_of_following': t[1]}
            return d, 201

    @marshal_with(follower_count)
    def delete(self, user_id, f_user_id):
        try:
            user_manager.remove_user_follower(f_user_id, user_id)
            user_manager.remove_user_following(user_id, f_user_id)
        except Exception as e:
            print('exception arrived during like deleteion r', e)
            return 'error', 500
            # pass  # TODO: Raise valid http excpiton
        else:
            t = user_manager.get_user_post_flr_flwing_count(f_user_id)
            print('API count rec', t)
            d ={'num_followers': t[0], 'num_of_following': t[1]}
            return d, 201