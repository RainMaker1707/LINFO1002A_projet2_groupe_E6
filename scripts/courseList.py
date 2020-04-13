import sqlite3


def course_list(filename):
    """
    :param filename: db file path
    :return: a list of clean string of all courses in db
    """
    connection = sqlite3.connect(filename).cursor()
    lst = list()
    for row in connection.execute("SELECT DISTINCT(course) FROM submissions"):
        if len(row[0]) > 10:
            for i in range(len(row[0])):
                if row[0][i] == "-":
                    lst.append(row[0][:i])
        else:
            lst.append(row[0])
    connection.close()
    return lst


def courses_list_templating(filename):
    """
    :param filename: db file path
    :return: the part of html which define the side bar menu courses list
    """
    lst = course_list(filename)
    final_str = "<ul>\n<li>Liste des cours\n<ul>"
    for elem in lst:
        final_str += "<li><a href=\"#\">{0}</a></li>\n".format(elem)
    final_str += "</ul>\n</li>\n</ul>\n"
    return final_str
