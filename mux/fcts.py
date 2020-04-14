from random import randint
import sqlite3

def write_file(path,text):
    """
    path = string
    text = string

    write the string to the file in the path
    """
    with open(path, 'w') as file:
        file.write(text)

def read_file(path):
    """
    return one string with the entire file
    """
    content_str = ""
    try:
        with open(path, 'r') as file:
            for line in file:
                content_str += line
    except:
        pass
    return content_str

def date_format(date):
    """
    in: date string
    out: int number of minutes
    """
    #2020-01-10T21:18:29.522+0100

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

def get_data(filename,task):
    """
    return a tuple with the dates of beginig and end as ints
    + the list of dates in string "month/day",...
    """
    dates = {}
    lst = []
    c = sqlite3.connect(filename).cursor()
    for row in c.execute("SELECT task, submitted_on from submissions order by submitted_on"):
        if row[0] == task:
            lst.append(date_format(row[1]))
            dates[row[1][0:10].replace("-","/")] = None

    c.close()
    lst.sort()

    temp = ["" for i in range(lst[-1]-lst[0])]
    for i in dates:
        temp[date_format(i)-lst[0]-1] = i
        #values[date-data[0]-1] += 1

    return (lst[0],temp,lst)

def get_color():
    return(randint(50,200),randint(50,200),randint(50,200),0.7)