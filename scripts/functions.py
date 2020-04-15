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


def get_colors(number: int):
    """
    """
    increm = 255//(number//3)
    num = number//3
    if number % 3 != 0:
        num += number%3
    colors1 = []
    colors2 = []
    colors3 = []

    red_g = 255
    green_r = 0
    green_b = 255
    blue_g = 0
    blue_r = 255
    red_b = 0

    for i in range(num):
        #red/green
        colors1.append((red_g,green_r,0,0.8))

        red_g -= increm
        green_r += increm

        #green/blue
        colors2.append((0,green_b,blue_g,0.8))

        green_b -= increm
        blue_g += increm

        #blue/red
        colors2.append((red_b,0,blue_r,0.8))

        blue_r -= increm
        red_b += increm
    lst = colors1 + colors2 + colors3
    return lst[0:number]


def date_format(date: str):
    """
    :param date: string yyyy-mm-dd...
    :return: int number of days
    only works for dates between 2000 and 2099
    """
    temp = date[0:10]
    days = 0
    leap_months = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    normal_months = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

    leap_year = False
    if int(temp[0:4]) % 4 == 0 and int(temp[0:4]) % 100 == 0 and int(temp[0:4]) % 400 == 0:
        leap_year = True

    if leap_year:
        days += leap_months[int(date[5:7])-1]
    else:
        days += normal_months[int(date[5:7])-1]
    days += int(temp[8:10])
    days += int(temp[2:4])*365

    return days


def date_dic_to_list(dic: dict, days: int, day_1: int):
    """
    :param dic: dictionary
    :param days: the number of days between the first and laast entry
    :param day_1: date_format() of the first day
    :return: a list of all keys in the dic sorted with empty spaces for missing dates
    """
    lst = ["" for _ in range(days)]
    for elem in dic:
        lst[date_format(elem)-day_1-1] = elem
    return lst


def leap(year):
    leap_flag = False
    if year % 4 == 0:
        leap_flag = True
    if year % 100 == 0:
        leap_flag = False
    if year % 400 == 0:
        leap_flag = True
    return leap_flag

