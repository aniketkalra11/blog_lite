from model.common_model_object import p_m_m, user_manager
from controller.post_controller import *
from controller.user_controller import *
from app import cache, app
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})
app.app_context().push()

@cache.memoize(timeout=3000)
def cache_get_all_post():
    # list_post = c_get_user_post(user_id)
    # return list_post
		return 'string'

@cache.cached(timeout=10000, key_prefix="cache_get_post_by_post_id")
def cache_get_post_by_post_id(user_id:str, post_id:str):
    post_container = create_post_container_obj(user_id, post_id, True)
    return post_container