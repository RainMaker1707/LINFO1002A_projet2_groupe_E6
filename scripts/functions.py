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


def get_random_colors(number: int):
    """
    :param number: number of tuple
    :return: a list of tuple of color in rgba : (r(0, 250), g(0, 250), b(0, 250), a(0, 1))
    """
    lst = list()
    for i in range(number):
        lst.append((randint(30, 250), randint(0, 250), randint(0, 250), 0.8))
    return lst


def get_colors(number: int, base_color: int = False):
    """
    :param number: number of tuple > 0
    :param base_color: int between 0 and 360
    :return: a list o string "hsl(x, xx%, xx%)"
    """
    step = 60/number

    if not base_color:
        fist = randint(0, 360)
    else:
        fist = base_color

    lst = []
    for i in range(number):
        lst.append("hsl({0}, 90%, {1}%)".format(fist, 20+i*step))

    return lst[:number]


def date_format(date: str):
    """
    :param date: string 'yyyy-mm-dd'...
    :return: int number of days sice year 0
    """
    days = 0
    leap_months = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    normal_months = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if leap(int(date[:4])):
        days += leap_months[int(date[5:7])-1]
    else:
        days += normal_months[int(date[5:7])-1]
    days += int(date[8:10])
    days += int(date[2:4]) * 365 + leap_years(int(date[2:4]))
    return days


def leap_years(year: int):
    """
    """
    return year//4 - year//100 + year//400


def date_dic_to_list(dic: dict, days: int, day_1: int):
    """
    :param dic: dictionary with the keys as dates yyyy/mm/dd
    :param days: the number of days between the first and last entry
    :param day_1: date_format() of the first day (in chronologic order)
    :return: a list of all keys in the dic sorted with empty spaces for missing dates
    """
    if len(dic) == 1:
        for elem in dic:
            return [date_format(elem)]
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


def find_day(date):
    """
    :param date: a string of a date in the format yyyy/mm/dd
    :return: an int between 0 and 6 coresponding to the day
    """
    year_code = (int(date[2:4]) + (int(date[2:4]) // 4)) %7

    month_index = [None,0,3,3,6,1,4,6,2,5,0,3,5]
    month_code = month_index[int(date[5:7])]

    # julian calendar
    if int(date[0:4]) < 1752:
        century_code = (18 - int(date[1:2])) % 7
        if date[0:4] % 4 == 0:
            leap_code = 0
        else:
            leap_code = 1


    # gregorian calendar
    else:
        century_index = {"17":4,"18":2,"19":0,"20":6,"21":4,"22":2,"23":0}
        century_code = century_index[date[0:2]]
        if leap(int(date[0:4])):
            leap_code = 1
        else:
            leap_code = 1


    day = ((year_code+month_code+century_code+leap_code+int(date[-2:])) % 7) - 1
    if day < 0:
        day = 6
    return day