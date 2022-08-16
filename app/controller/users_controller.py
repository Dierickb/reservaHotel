from typing import List

from ..models.models import Login, User
from ..helpers import helper
from ..database import users_db


def validateLogin(user_: Login) -> bool:
    user = helper.format_login(user_)
    helper.validate_Login(user)
    return users_db.validateLogin("email", user)


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


def details(id: str) -> User:
    return users_db.detail(id)
