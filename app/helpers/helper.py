import re

from ..models.models import Login, User, Room
from ..models.exceptions import UserNotValid, RoomNotValid


def validate_Login(user: Login) -> None:
    if not __email_is_valid(user.email):
        raise UserNotValid(f"The email: {user.email} is not valid")

    if not __password_is_valid(user.password):
        raise UserNotValid("The password is not valid")


def format_login(user: Login) -> Login:
    user_dict = user._asdict()
    user_dict["email"] = user.email.lower()
    user_dict["password"] = user.password

    return Login(**user_dict)


def format_user(user: User) -> User:
    user_dict = user._asdict()
    user_dict["email"] = user.email.lower()
    user_dict["password"] = user.password

    return User(**user_dict)


def format_name(user: User) -> User:
    contact_dict = user._asdict()
    contact_dict["fullName"] = user.fullName.capitalize()

    return User(**contact_dict)


def format_room(room: Room) -> Room:
    room_dict = room._asdict()
    room_dict["location"] = room.location
    room_dict["id"] = room.id
    room_dict["available"] = room.available

    return Room(**room_dict)


def validate_user(user: User) -> None:
    if not __email_is_valid(user.email):
        raise UserNotValid(f"The email address: {user.email} is not valid")

    if None in (user.fullName, user.email):
        raise UserNotValid("The user has no full name or email")

    if is_empty(user.password):
        raise UserNotValid("The user has no password")

    if is_empty(user.phone):
        raise UserNotValid("The user has no phone")

    if is_empty(user.rol):
        raise UserNotValid("The user has no rol")


def validate_room(room: Room) -> None:
    for clave in room:
        if room[clave].isEmpty() | len(room[clave]) == 0:
            raise RoomNotValid(f"The {clave} should not be empty")


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


def is_empty(a):
    return not a


def __image_to_binary(imagePath):
    with open(imagePath, 'rb') as f:
        blob = f.read()
    return blob
