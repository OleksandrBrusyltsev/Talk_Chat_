from typing import Type
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import BlacklistMixin, Token
from chat.service.action_token_enum import ActionEnum
from chat.service.jwt_exeption import JWTException
from authentication.models import CustomUser as User
from typing import Type, Union

CustomUser: User = get_user_model()

ActionTokenClassType = Type[Union[BlacklistMixin, Token]]


class ActionToken(BlacklistMixin, Token):
    pass


class ActivateToken(ActionToken):
    lifetime = ActionEnum.ACTIVATE.exp_time

    token_type = ActionEnum.ACTIVATE.token_type


class RecoveryPasswordToken(ActionToken):
    lifetime = ActionEnum.RECOVERY_PASSWORD.exp_time

    token_type = ActionEnum.RECOVERY_PASSWORD.token_type


class SocketToken(ActionToken):
    token_type = ActionEnum.SOCKET.token_type
    lifetime = ActionEnum.SOCKET.exp_time


class JWTService:

    @staticmethod
    def create_token(user, token_class: ActionTokenClassType):

        return token_class.for_user(user)

    @staticmethod
    def validate_token(token, token_class: ActionTokenClassType):
        try:

            token_res = token_class(token)

            token_res.check_blacklist()
        except (Exception,):
            raise JWTException

        token_res.blacklist()

        user_id = token_res.payload.get('user_id')

        return get_object_or_404(CustomUser, pk=user_id)
