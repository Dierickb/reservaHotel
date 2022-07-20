from typing import List

from ..models.models import Login
from ..helpers import helper


def validateUser(user_: Login) -> Login:
    user = helper.format_user(user_)
    helper.validate_Login(user)
    return user_
