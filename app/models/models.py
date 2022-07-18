from typing import NamedTuple, Optional


class Login(NamedTuple):
    nickName: Optional[str] = None
    password: Optional[str] = None
