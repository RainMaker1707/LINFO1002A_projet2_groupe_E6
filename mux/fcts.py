import sqlite3


def date_format(date):
    """
    :param date: string
    :return: int number of minutes
    """
    temp = date[0:10]
    days = 0
    if temp[0:4] == "2020":
        days += 365

        if temp[5:7] == "02":
            days += 31
        elif temp[5:7] == "03":
            days += 60
        elif temp[5:7] == "04":
            days += 91
        elif temp[5:7] == "05":
            days += 121
        elif temp[5:7] == "06":
            days += 152
        elif temp[5:7] == "07":
            days += 182
        elif temp[5:7] == "08":
            days += 213
        elif temp[5:7] == "09":
            days += 244
        elif temp[5:7] == "10":
            days += 274
        elif temp[5:7] == "11":
            days += 305
        elif temp[5:7] == "12":
            days += 335
    else:
        if temp[5:7] == "02":
            days += 31
        elif temp[5:7] == "03":
            days += 59
        elif temp[5:7] == "04":
            days += 90
        elif temp[5:7] == "05":
            days += 120
        elif temp[5:7] == "06":
            days += 151
        elif temp[5:7] == "07":
            days += 181
        elif temp[5:7] == "08":
            days += 212
        elif temp[5:7] == "09":
            days += 243
        elif temp[5:7] == "10":
            days += 273
        elif temp[5:7] == "11":
            days += 304
        elif temp[5:7] == "12":
            days += 334
    days += int(temp[8:10])
    return days


def get_data(filename, task):
    """
    :param filename:
    :param task:
    :return a tuple with the dates of beginning and end as ints + the list of dates in string "month/day",...
    """
    dates = {}
    lst = []
    c = sqlite3.connect(filename).cursor()
    for row in c.execute("SELECT task, submitted_on from submissions order by submitted_on WHERE task='{0}'"
                         .format(task)):
        lst.append(date_format(row[1]))
        dates[row[1][0:10].replace("-", "/")] = None
    c.close()
    lst.sort()
    temp = ["" for _ in range(lst[-1]-lst[0])]
    for elem in dates:
        temp[date_format(elem)-lst[0]-1] = elem
    return lst[0], temp, lst


def get_entries(filename, task):
    """
    return list of entries
    [(/entry/),(course,task,date,username,result)]
    """
    lst = []
    c = sqlite3.connect(filename).cursor()
    for row in c.execute("SELECT task, username, result from submissions WHERE task='{0}'ORDER BY submitted_on ASC".format(task)):
        lst.append(row)
    c.close()
    return lst
