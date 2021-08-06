from sqlite3 import Cursor
from typing import Union
import sqlite3

__all__ = ['get_best', 'insert_result', 'cursor']


def get_best(count: int = 0) -> dict[int: tuple[Union[None, str], int]]:
    """ Returns the result of the top 3 players. """
    try:
        assert -1 <= count <= 3
    except AssertionError:
        raise ValueError('Invalid argument count, must be no more than 3 and no less than -1')
    cursor.execute("""
    SELECT name gamer, max(score) score FROM RECORDS
    GROUP by name
    ORDER by score DESC
    LIMIT 3
    """)
    source = cursor.fetchall()
    sparse_arr = [source[i] for i in range(len(source)) if len(source) >= 1] + [(None, -1)] * (3 - len(source))
    result = {i: dict(name=sparse_arr[i - 1][0], score=sparse_arr[i - 1][1]) for i in range(1, 4)}
    return result if count == 0 else result[count]


def insert_result(name: str, score: int) -> None:
    """ Inserts new data into the SQL table, saving it.

     name: name of the player
    score: record value
    """
    cursor.execute("""
    insert into RECORDS values ( ?, ?)
    """, (name, score))
    BD.commit()


BD = sqlite3.connect("2048.sqlite")

cursor: Cursor = BD.cursor()
cursor.execute("""
create table if not exists RECORDS (
    name text,
    score integer
)
""")
