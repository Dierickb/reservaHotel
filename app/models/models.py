from datetime import datetime
from typing import NamedTuple, Optional


class Login(NamedTuple):
    email: Optional[str] = None
    password: Optional[str] = None


class Date(NamedTuple):
    initDate: Optional[datetime.date] = None
    finalDate: Optional[str] = None


class User(NamedTuple):
    id: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    fullName: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
