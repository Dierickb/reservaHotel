from typing import List

from .connection import _fetch_all, _fetch_lastrow_id, _fetch_none, _fetch_one
from ..models.models import Login, User
from ..models.exceptions import UserAlreadyExists, UserNotFound
from ..helpers.helper import is_empty

from faker import Faker


def create(user: User) -> User:
    if validateUser("email", user.email):
        raise UserAlreadyExists(f"Email {user.email} is already used")

    query = """INSERT INTO users VALUES (:email, :password, :fullName, :phone, :address)"""

    user_dict = user._asdict()

    id_ = _fetch_lastrow_id(query, user_dict)

    user_dict["id"] = id_
    return user  # User(**user_dict)


def update(user_: User) -> User:
    if not validateUser("oid", user_.id):
        raise UserNotFound("User not Found!")

    user = validateUpdate("oid", user_)

    query = """UPDATE users SET email = :email, password = :password,
                      fullName = :fullName, phone = :phone, address = :address
               WHERE oid = :oid"""

    parameters = user._asdict()

    _fetch_none(query, parameters)

    return user_


def delete(user: User) -> User:
    if not validateUser("oid", user.id):
        raise UserNotFound("User not Found!")

    query = "DELETE FROM users WHERE oid = ?"
    parameters = [user.id]

    _fetch_none(query, parameters)

    return user


def list_all() -> List[User]:
    query = "SELECT oid, * FROM users"
    records = _fetch_all(query)

    users = []
    for record in records:
        user = User(id=record[0], email=record[1], password=record[2],
                    fullName=record[3], phone=record[4], address=record[5])
        users.append(user)

    return users


def detail(user: User) -> User:
    query = "SELECT oid, * FROM users WHERE oid=?"
    parameters = [user.id]

    record = _fetch_one(query, parameters)

    if record is None:
        raise UserNotFound(f"No user with id: {user.id}")

    user = User(id=record[0], email=record[1], password=record[2],
                fullName=record[3], phone=record[4], address=record[5])

    return user


def validateUser(field: str, value: str) -> bool:
    query = f"SELECT oid, email FROM users WHERE {field}=?"
    parameters = [value]

    record = _fetch_one(query, parameters)

    return bool(record)


def validateLogin(field: str, value: Login) -> bool:
    query = f"SELECT email, password FROM users WHERE {field}=?"
    parameters = [value.email]

    record = _fetch_one(query, parameters)

    if not bool(record):
        raise UserNotFound(f"User with email {value.email} was not found")

    return record


def validateUpdate(field: str, value: User) -> User:
    query = f"SELECT oid, email FROM users WHERE {field}=?"
    parameters = [value.id]

    record = _fetch_one(query, parameters)

    user_db = User(id=record[0], email=record[1], password=record[2],
                   fullName=record[3], phone=record[4], address=record[5])

    if is_empty(value.email):
        value.email = user_db.email

    if is_empty(value.password):
        value.password = user_db.password

    if is_empty(value.fullName):
        value.fullName = user_db.fullName

    if is_empty(value.phone):
        value.phone = user_db.phone

    if is_empty(value.address):
        value.address = user_db.address

    return value


def reset_table() -> None:
    query = "DROP TABLE IF EXISTS users"
    _fetch_none(query)

    fields = """(email text, password text, fullName text, phone int, address text)"""
    query = f"CREATE TABLE IF NOT EXISTS users {fields}"
    _fetch_none(query)

    fake = Faker()
    fake.seed_instance(42)

    for _ in range(10):
        test_user = User(email=fake.email(), password=fake.password(),
                         fullName=fake.first_name(), phone=fake.phone_number(),
                         address=fake.street_address())

        create(test_user)
