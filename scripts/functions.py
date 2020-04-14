from random import randint
import sqlite3


def request(filename: str, req: str):
    """
    :param filename: filename of the data base
    :param req: SQL request to send to bdd
    :return: a list of the tuple gave from SQL request
    """
    connection = sqlite3.connect(filename).cursor()
    lst = list()
    for row in connection.execute(req):
        lst.append(row)
    connection.close()
    return lst


def format_request_where(req: str, where_arg: str):
    """
    :param req: SQL request to format
    :param where_arg: arg to set at WHERE="where_arg"
    :return: str: a clean SQL request with set WHERE
    """
    return req.replace("WHERE ", "WHERE {0}".format(where_arg))


def get_random_colors(number: int):
    """
    :param number: number of tuple
    :return: a list of tuple of color in rgba : (r(0, 250), g(0, 250), b(0, 250), a(0, 1))
    """
    lst = list()
    for i in range(number):
        lst.append((randint(0, 250), randint(0, 250), randint(0, 250), 0.8))
    return lst
