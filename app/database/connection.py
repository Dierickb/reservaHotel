from __future__ import annotations
from contextlib import contextmanager
from typing import Any, Iterator, List, Optional


import sqlite3

from config import Config

DATABASE_PATH = Config.DATABASE_PATH


@contextmanager
def __get_cursor() -> Iterator[sqlite3.Cursor]:  # Manejador de eventos
    connection: sqlite3.Connection = sqlite3.connect(DATABASE_PATH)  # se abre la conexion
    cursor: sqlite3.Cursor = connection.cursor()  # Definimos el cursor de la conexion
    try:
        yield cursor
        connection.commit()
    finally:  # Cierro la conexion ya sea que se realice correctamente o falle
        cursor.close()
        connection.close()


def _fetch_one(query: str, parameters: Optional[List[str] | Optional[List[int]]] = None ) -> Any:
    if parameters is None:
        parameters = []

    with __get_cursor() as cursor:
        cursor.execute(query, parameters)
        return cursor.fetchone()


def _fetch_all(query: str, parameters: Optional[List[str]] = None) -> List:
    if parameters is None:
        parameters = []

    with __get_cursor() as cursor:
        cursor.execute(query, parameters)
        return cursor.fetchall()


def _fetch_none(query: str, parameters: Optional[List[str]] | Any = None) -> None:
    if parameters is None:
        parameters = []

    with __get_cursor() as cursor:
        cursor.execute(query, parameters)


def _fetch_lastrow_id(query: str, parameters: Optional[List[str]] | Any = None) -> int:
    if parameters is None:
        parameters = []

    with __get_cursor() as cursor:
        cursor.execute(query, parameters)
        return cursor.lastrowid
