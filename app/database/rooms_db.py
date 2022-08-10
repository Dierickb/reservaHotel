import os
from typing import List

from .connection import _fetch_all, _fetch_lastrow_id, _fetch_none, _fetch_one
from ..models.models import Room
from ..models.exceptions import RoomAlreadyExists, RoomNotFound
from ..helpers.helper import __image_to_binary

from faker import Faker


def create(room: Room) -> Room:
    if validateRoom("oid", room.id):
        raise RoomAlreadyExists(f"Room in the floor {room.id} already exist")

    query = """INSERT INTO rooms VALUES (:floor, :cantBathroom, :guests, :typeRoom, 
    :possibilities, :available, :photo)"""

    room_dict = room._asdict()

    id_ = _fetch_lastrow_id(query, room_dict)

    room_dict["id"] = id_
    return room  # Room(**room_dict)


def update(room: Room) -> Room:
    if not validateRoom("oid", room.id):
        raise RoomNotFound(f"The room with id {room.id} does not exist")

    query = """UPDATE rooms SET floor = :floor, cantBathroom = :cantBathroom,
                  guests = :guests, typeRoom = :typeRoom, possibilities = :possibilities, 
                  available = :available, photo = :photo
                WHERE oid = :oid"""

    room_dict = room._asdict()

    id_ = _fetch_lastrow_id(query, room_dict)

    room_dict["id"] = id_
    return room  # Room(**)


def delete(room: Room) -> Room:
    if not validateRoom("oid", room.id):
        raise RoomNotFound(f"The room with id {room.id} does not exist")

    query = "DELETE FROM users WHERE oid = ?"
    parameters = [room.id]

    _fetch_none(query, parameters)

    return room


def list_all() -> List[Room]:
    query = "SELECT oid, * FROM rooms"
    records = _fetch_all(query)

    rooms = []
    for record in records:
        room = Room(id=record[0], floor=record[1], cantBathroom=record[2],
                    guests=record[3], typeRoom=record[4], possibilities=record[5],
                    available=record[6], photo=record[7])
        rooms.append(room)

    return rooms


def detail(room: Room) -> Room:
    query = "SELECT oid, * FROM rooms WHERE oid=?"
    parameters = [room.id]

    record = _fetch_one(query, parameters)

    if record is None:
        raise RoomNotFound(f"The room with id {room.id} does not exist")

    room = Room(id=record[0], floor=record[1], cantBathroom=record[2],
                guests=record[3], typeRoom=record[4], possibilities=record[5],
                available=record[6], photo=record[7])

    return room


def validateRoom(field: str, value: str | int) -> bool:
    query = f"SELECT oid FROM rooms WHERE {field}=?"
    parameters = [value]

    record = _fetch_one(query, parameters)

    return bool(record)


def reset_room_table() -> None:
    query = "DROP TABLE IF EXISTS rooms"
    _fetch_none(query)

    fields = """(floor id, cantBathroom int, guests int, typeRoom str, possibilities int, 
    available int, photo BLOB NOT NULL) """
    query = f"CREATE TABLE IF NOT EXISTS rooms {fields}"
    _fetch_none(query)

    base_path = os.path.dirname(__file__)
    upload_path = os.path.join(base_path, '../views/static/img/icons8-hamburger-48.png')
    image_in_binary = __image_to_binary(upload_path)

    fake = Faker()
    fake.seed_instance(42)

    for _ in range(10):
        test_room = Room(floor=2, cantBathroom=2, guests=1, typeRoom="individual", possibilities=2,
                         available=1, photo=image_in_binary)

        create(test_room)
