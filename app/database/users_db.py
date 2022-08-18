from typing import List

from .connection import _fetch_all, _fetch_lastrow_id, _fetch_none, _fetch_one
from ..models.models import Login, User
from ..models.exceptions import UserAlreadyExists, UserNotFound
from ..helpers.helper import is_empty
from werkzeug.security import generate_password_hash, check_password_hash

from faker import Faker


def create(user: User) -> User:
    if validateUser("usCorreo", user.email):
        raise UserAlreadyExists(f"Email {user.email} is already used")

    query = """INSERT INTO USUARIOS (usCorreo, usContrasena, usNombre, usContacto, usRol)

    VALUES (:email, :password, :fullName, :phone, :rol)"""

    user_dict = user._asdict()

    id_ = _fetch_lastrow_id(query, user_dict)

    user_dict["id"] = id_
    return User(**user_dict)  # User(**user_dict)


def update(user_: User) -> User:
    if not validateUser("usId", user_.id):
        raise UserNotFound("User not Found!")

    user = validateUpdate("usId", user_)

    query = """UPDATE USUARIOS SET usCorreo = :email, usContrasena = :password,
                      usNombre = :fullName, usContacto = :phone, usRol = :rol
               WHERE usId = :id"""

    parameters = user._asdict()

    _fetch_none(query, parameters)

    return user_


def delete(user: User) -> User:
    if not validateUser("usId", user.id):
        raise UserNotFound("User not Found!")

    query = "DELETE FROM USUARIOS WHERE usId = ?"
    parameters = [user.id]

    _fetch_none(query, parameters)

    return user


def list_all() -> List[User]:
    query = "SELECT * FROM USUARIOS"
    records = _fetch_all(query)
    users = []
    for record in records:
        user = User(id=record[0], fullName=record[1], phone=record[2],
                    email=record[3], rol=record[4], password=record[5])
        users.append(user)

    return users


def detail(userId: int) -> User:
    parameters = [userId]
    if userId == 0:
        query = "SELECT * FROM USUARIOS WHERE usId= (SELECT max(usId) FROM USUARIOS)"
        record = _fetch_one(query)
    else:
        query = "SELECT * FROM USUARIOS WHERE usId=?"
        record = _fetch_one(query, parameters)

    if record is None:
        raise UserNotFound(f"No user with id: {userId}")

    user = User(id=record[0], fullName=record[1], phone=record[2],
                email=record[3], rol=record[4], password=record[5])

    return user


def validateUser(field: str, value: str | int) -> bool:
    query = f"SELECT usCorreo FROM USUARIOS WHERE {field}=?"
    parameters = [value]

    record = _fetch_one(query, parameters)

    return bool(record)


def validateLogin(field: str, value: Login) -> Login:
    query = f"SELECT usCorreo, usContrasena, usRol, usId FROM USUARIOS WHERE {field}=?"
    parameters = [value.email]

    record = _fetch_one(query, parameters)

    if not bool(record):
        raise UserNotFound(f"User with email {value.email} was not found")

    userLogIn = Login(email=record[0], password=record[1], rol=record[2],id=record[3])

    return userLogIn


def validateUpdate(field: str, value: User) -> User:
    query = f"SELECT usId, usCorreo, usContrasena, usNombre, usContacto, usRol FROM USUARIOS WHERE {field}=?"
    parameters = [value.id]

    record = _fetch_one(query, parameters)

    user_db = User(id=record[0], email=record[1], password=record[2],
                   fullName=record[3], phone=record[4], rol=record[5])

    if is_empty(value.email):
        value.email = user_db.email

    if is_empty(value.password):
        value.password = user_db.password

    if is_empty(value.fullName):
        value.fullName = user_db.fullName

    if is_empty(value.phone):
        value.phone = user_db.phone

    if is_empty(value.rol):
        value.address = user_db.rol

    return value


def reset_table() -> None:
    print("DireickS")
    # query = "DROP TABLE IF EXISTS users"
    # _fetch_none(query)

    # fields = """(email text, password text, fullName text, phone int, address text)"""
    # query = f"CREATE TABLE IF NOT EXISTS users {fields}"
    # _fetch_none(query)

    fake = Faker()
    fake.seed_instance(42)

    for _ in range(10):
        test_user = User(email=fake.email(), password=generate_password_hash("admin"),
                         fullName=fake.first_name(), phone=fake.phone_number(),
                         rol="admin")
        create(test_user)
