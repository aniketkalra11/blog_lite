from .post_model_controller import PostModelManager
from .user_model_controller import UserModelManager
from .user_behaviour_controller import UserBehaviourController
from .user_behaviour_controller import UserTokenManager

p_m_m = PostModelManager()
user_manager = UserModelManager()
user_behaviour_manager = UserBehaviourController()
user_token_manager = UserTokenManager()
