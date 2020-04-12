import sqlite3


def connection(filename):
    return sqlite3.connect(filename).cursor()

