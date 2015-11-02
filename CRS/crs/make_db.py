import sqlite3
import os
import sys
from crs.settings import DB_NAME, SQL_COMMANDS


def create_db(path):
    path += '/' + DB_NAME
    if os.path.exists(path):
        os.remove(path)

    conn = sqlite3.connect(path)
    c = conn.cursor()
    with open(SQL_COMMANDS) as info:
        script = info.read()
        c.executescript(script)


if __name__ == '__main__':
    create_db(os.path.dirname(os.path.realpath(__file__)))
