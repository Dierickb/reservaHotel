from typing import List

from ..models.models import Room
from ..helpers import helper
from ..database import rooms_db


def validateRoom(room_: Room) -> bool:
    room = helper.format_room(room_)
    return rooms_db.validateRoom("floor", room.floor)


def create(room_: Room) -> Room:
    room = helper.format_room(room_)
    return rooms_db.create(room)


def update(room_: Room) -> Room:
    room = helper.format_room(room_)
    return rooms_db.update(room)


def delete(room_: Room) -> Room:
    return rooms_db.delete(room_)


def lists() -> List[Room]:
    return rooms_db.list_all()


def details(room_: Room) -> Room:
    return rooms_db.detail(room_)
