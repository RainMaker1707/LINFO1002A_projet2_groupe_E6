from flask import Flask, render_template, url_for
from scripts.courseList import *
from scripts.makeGraph import *
app = Flask(__name__, template_folder='templates', static_folder='style')


@app.route('/')
def home():
    """
    :return:
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
                                                 "TEST TITLE", "graph3", False),
                           GRAPH4=top_subs_count(db, 1000, "line",
                                                 "SELECT SUM(tried), course, username  FROM user_tasks "
                                                 "GROUP BY username, course",
                                                 "TEST TITLE", "graph4", False),
                           MENU=make_menu(db))


@app.route('/course/<course>')
def course_page(course: str):
    db = "scripts/DataBase/inginious.sqlite"
    course = request(db, "SELECT DISTINCT(course) FROM user_tasks WHERE course LIKE \"{0}%\"".format(course))[0][0]
    req_fail = "SELECT DISTINCT(task), COUNT(result) FROM submissions WHERE course='{0}' GROUP BY task".format(course)
    req_success = "SELECT DISTINCT(task), COUNT(result) FROM submissions " \
                  "WHERE course='{0}'  AND result='success' GROUP BY task".format(course)
    return render_template("base.html", STYLE=url_for('static', filename="base.css"), MENU=make_menu(db),
                           PATH="\t<a href=\"/\">  Statistics  </a>|"
                                "<a href=\"/course/{0}\">  {0}  </a>\t".format(course),
                           GRAPH3=double_bar_graph(db, req_fail, req_success),
                           GRAPH4=top_subs_count(db, 500, "line",
                                                 "SELECT SUM(tried), task, username FROM user_tasks "
                                                 "WHERE course='{0}' GROUP BY username, task ".format(course),
                                                 "TEST TITLE", "graph4", True)
                           )


@app.route('/course/<course>/<task>')
def task_page(course: str, task: str):
    db = "scripts/DataBase/inginious.sqlite"
    return render_template("base.html", STYLE=url_for('static', filename="base.css"), MENU=make_menu(db),
                           PATH="\t<a href=\"/\">  Statistics  </a>|<a href=\"/course/{0}\">  {0}  "
                                "</a>|<a href=\"/course/{0}/{1}\">  {1}  </a>".format(
                               course, task),
                           GRAPH1=student_perform_graph(db, task),
                           GRAPH2=best_user_perf(db, task),
                           GRAPH3=graph_submissions_repartition(db, task))
