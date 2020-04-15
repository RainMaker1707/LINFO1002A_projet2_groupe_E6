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
    if int(temp[0:4]) % 4 == 0:
        if int(temp[0:4]) % 100 == 0:
            if int(temp[0:4]) % 400 == 0:
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
