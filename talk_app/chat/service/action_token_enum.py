from datetime import timedelta
from enum import Enum


class ActionEnum(Enum):

    ACTIVATE = ('activate', timedelta(days=1))
    RECOVERY_PASSWORD = ('recovery_password', timedelta(hours=1))
    SOCKET = ('socket', timedelta(minutes=1))

    def __init__(self, token_type, exp_time):
        self.token_type = token_type
        self.exp_time = exp_time

