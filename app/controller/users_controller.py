from typing import List

from ..models.models import Login, User
from ..helpers import helper
from ..database import users_db


def validateLogin(user_: Login) -> Login:
    user = helper.format_login(user_)
    helper.validate_Login(user)
    return users_db.validateLogin("usCorreo", user)


def create(user_: User) -> User:
    user = helper.format_user(user_)
    helper.validate_user(user)
    return users_db.create(user)


def update(user_: User) -> User:
    user_ = helper.format_name(user_)
    helper.validate_user(user_)
    return users_db.update(user_)


def delete(contact: User) -> User:
    return users_db.delete(contact)


def lists() -> List[User]:
    return users_db.list_all()


def details(userId: int) -> User:
    return users_db.detail(userId)
