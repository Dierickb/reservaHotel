import os
from typing import List

from .connection import _fetch_all, _fetch_lastrow_id, _fetch_none, _fetch_one
from ..models.models import Room
from ..models.exceptions import RoomAlreadyExists, RoomNotFound
from ..helpers.helper import __image_to_binary

from faker import Faker


def create(room: Room) -> Room:
    if validateRoom("hbId", room.id):
        raise RoomAlreadyExists(f"Room in the floor {room.id} already exist")
    query = """INSERT INTO HABITACIONES (hbLocaliacion, hbDisponible) 
                VALUES (:location, :available)"""

    room_dict = room._asdict()

    id_ = _fetch_lastrow_id(query, room_dict)

    room_dict["id"] = id_
    return Room(**room_dict)  # Room(**room_dict)


def update(room: Room) -> Room:
    if not validateRoom("hbId", room.id):
        raise RoomNotFound(f"The room with id {room.id} does not exist")

    query = """UPDATE rooms SET hbLocalizacion = :location, 
                                hbDisponible = :available
                WHERE hbId = :id"""

    room_dict = room._asdict()

    id_ = _fetch_lastrow_id(query, room_dict)

    room_dict["id"] = id_
    return Room(**room_dict)  # Room(**)


def delete(room: Room) -> Room:
    if not validateRoom("hbId", room.id):
        raise RoomNotFound(f"The room with id {room.id} does not exist")

    query = "DELETE FROM HABITACIONES WHERE hbId = ?"
    parameters = [room.id]

    _fetch_none(query, parameters)

    return room


def list_all() -> List[Room]:
    query = "SELECT * FROM HABITACIONES"
    records = _fetch_all(query)

    rooms = []
    for record in records:
        room = Room(id=record[0], location=record[1], available=record[2])
        rooms.append(room)

    return rooms


def detail(room: Room) -> Room:
    query = "SELECT * FROM HABITACIONES WHERE hbId=?"
    parameters = [room.id]

    record = _fetch_one(query, parameters)

    if record is None:
        raise RoomNotFound(f"The room with id {room.id} does not exist")

    room = Room(id=record[0], location=record[1], available=record[2])

    return room


def validateRoom(field: str, value: str | int) -> bool:
    query = f"SELECT hbId FROM rooms WHERE {field}=?"
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
