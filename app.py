from flask import Flask, render_template, url_for
from scripts.courseList import *
from scripts.makeGraph import *

app = Flask(__name__, template_folder='templates', static_folder='style')


@app.route('/')
def home():
    """
    :return: the html home page
    """
    db = "scripts/DataBase/inginious.sqlite"
    return render_template("base.html",
                           STYLE=url_for('static', filename="base.css"),
                           PATH="\t<a href=\"#\">  Statistics  </a>",
                           GRAPH1=double_bar_graph(db, "SELECT course, COUNT(result) FROM submissions GROUP BY course",
                                                   "SELECT course, COUNT(result) FROM submissions WHERE "
                                                   "result=\"success\" GROUP BY course"),
                           GRAPH2=graph_total_sub(db),
                           GRAPH3=top_subs_count(db, 50, "bar",
                                                 "SELECT SUM(tried), username FROM user_tasks GROUP BY username",
                                                 "Podium of student with smallest submissions numbers",
                                                 "graph3", False),
                           GRAPH4=top_subs_count(db, 50, "bar",
                                                 "SELECT SUM(tried), course, username FROM user_tasks "
                                                 "GROUP BY username, course",
                                                 "Podium of student with highest submissions numbers per course",
                                                 "graph4", True),
                           MENU=make_menu(db))


@app.route('/course/<course>')
def course_page(course: str):
    """
    :param course: string name of the current course
    :return: the html course page filled with goods graphs
    """
    db = "scripts/DataBase/inginious.sqlite"
    course_lst = course_list(db)
    if course not in course_lst:
        return render_template("base.html", STYLE=url_for('static', filename="base.css"), MENU=make_menu(db),
                               PATH="\t<a href=\"/\">  Statistics  </a>|  COURSE NOT FOUND",
                               GRAPH3="<p style=\"color: #E99002\">ERROR 404 course not found</p>")

    course = request(db, "SELECT DISTINCT(course) FROM user_tasks WHERE course LIKE \"{0}%\"".format(course))[0][0]
    req_fail = "SELECT DISTINCT(task), COUNT(result) FROM submissions WHERE course='{0}' GROUP BY task".format(course)
    req_success = "SELECT DISTINCT(task), COUNT(result) FROM submissions " \
                  "WHERE course='{0}'  AND result='success' GROUP BY task".format(course)
    return render_template("base.html", STYLE=url_for('static', filename="base.css"), MENU=make_menu(db),
                           PATH="\t<a href=\"/\">  Statistics  </a>|"
                                "<a href=\"/course/{0}\">  {0}  </a>\t".format(course),
                           GRAPH3=double_bar_graph(db, req_fail, req_success),
                           GRAPH4=top_subs_count(db, 50, "bar",
                                                 "SELECT SUM(tried), task, username FROM user_tasks "
                                                 "WHERE course='{0}' GROUP BY username, task ".format(course),
                                                 "Podium of student with highest submissions numbers per task",
                                                 "graph4", True),
                           GRAPH1=graph_week_distribution(db, course),
                           GRAPH2=graph_day_distribution(db, course))


@app.route('/course/<course>/<task>')
def task_page(course: str, task: str):
    """
    :param course:  string name of the current course
    :param task:  string name of the current task
    :return: the html task page filled with goods graphs
    """
    db = "scripts/DataBase/inginious.sqlite"
    if course not in course_list(db):
        return render_template("base.html", STYLE=url_for('static', filename="base.css"), MENU=make_menu(db),
                               PATH="\t<a href=\"/\">  Statistics  </a>| COURSE NOT FOUND",
                               GRAPH3="<p style=\"color: #E99002\">ERROR 404 course not found</p>")

    if task not in tasks_list(db, course):
        return render_template("base.html", STYLE=url_for('static', filename="base.css"), MENU=make_menu(db),
                               PATH="\t<a href=\"/\">  Statistics  </a>|  <a href=\"/course/{0}\">{0} </a> |"
                                    " TASK NOT FOUND".format(course),
                               GRAPH3="<p style=\"color: #E99002\">ERROR 404 task not found</p>")

    return render_template("base.html", STYLE=url_for('static', filename="base.css"), MENU=make_menu(db),
                           PATH="\t<a href=\"/\">  Statistics  </a>|<a href=\"/course/{0}\">  {0}  "
                                "</a>|<a href=\"/course/{0}/{1}\">  {1}  </a>".format(
                               course, task),
                           GRAPH1=student_perform_graph(db, task),
                           GRAPH2=best_user_perf(db, task),
                           GRAPH3=graph_submissions_distribution(db, task),
                           GRAPH4=graph_error_distribution(db, task))
