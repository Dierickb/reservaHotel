import re

from ..models.models import Login
from ..models.exceptions import UserNotValid


def validate_Login(user: Login) -> None:
    if not __nickName_is_valid(user.nickName):
        raise UserNotValid(f"The nickName: {user.nickName} is not valid")

    if not __password_is_valid(user.password):
        raise UserNotValid("The password is not valid")


def format_user(user: Login) -> Login:
    user_dict = user._asdict()
    user_dict["nickName"] = user.nickName.capitalize()
    user_dict["password"] = user.password.capitalize()

    return Login(**user_dict)


def __nickName_is_valid(nickName: str) -> bool:
    if not isinstance(nickName, str):
        return False

    # regex = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    regex = r'^(\w|\.|\_|\-)'

    return bool(re.search(regex, nickName))


def __password_is_valid(password: str) -> bool:
    if not isinstance(password, str):
        return False

    # regex = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    regex = r'^(\w|\.|\_|\-)'

    return bool(re.search(regex, password))
