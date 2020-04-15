from scripts.functions import request
import sqlite3


def course_list(filename: str):
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


def tasks_list(filename: str, course: str):
    tasks = request(filename,
                    "SELECT distinct(task) FROM user_tasks WHERE course LIKE '{0}%' GROUP BY task".format(course))
    for i in range(len(tasks)):
        tasks[i] = tasks[i][0]
    return tasks


def make_menu(filename: str):
    """
    :param filename: db file path
    :return: the part of html which define the side bar menu courses list
    """
    course_lst = course_list(filename)
    final_str = "<ul>\n<li>Courses List\n<ul>"
    for course in course_lst:
        final_str += "<li><div class='dropButton'> > </div><a href=\"/course/{0}\">{0}</a><ul>\n".format(course)
        task_lst = tasks_list(filename, course)
        if task_lst:
            final_str += "<div class='task'>\n"
        for task in task_lst:
            final_str += "\t<li><a href=\"/course/{0}/{1}\">{1}</a></li>\n".format(course, task)
        if task_lst:
            final_str += "</ul>\n</li>\n</div>\n"
    final_str += "</ul>\n</li>\n</ul>\n"
    final_str += "<script>\n\t$(\"nav ul li ul\").click(function()"
    final_str += "{\n\t$(this).toggleClass(\"active\");\t\n\t})\n;</script>"
    return final_str
