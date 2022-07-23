import re

from ..models.models import Login
from ..models.exceptions import UserNotValid


def validate_Login(user: Login) -> None:
    if not __email_is_valid(user.email):
        raise UserNotValid(f"The email: {user.email} is not valid")

    if not __password_is_valid(user.password):
        raise UserNotValid("The password is not valid")


def format_user(user: Login) -> Login:
    user_dict = user._asdict()
    user_dict["email"] = user.email.capitalize()
    user_dict["password"] = user.password.capitalize()

    return Login(**user_dict)


def __email_is_valid(email: str) -> bool:
    if not isinstance(email, str):
        return False

    regex = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    return bool(re.search(regex, email))


def __password_is_valid(password: str) -> bool:
    if not isinstance(password, str):
        return False

    # regex = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    regex = r'^(\w|\.|\_|\-)'

    return bool(re.search(regex, password))
