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
                           GRAPH1=double_bar_graph(db, "SELECT course, COUNT(result) FROM submissions GROUP BY course",
                                                   "SELECT course, COUNT(result) FROM submissions WHERE "
                                                   "result=\"success\" GROUP BY course"),
                           GRAPH2=graph_total_sub(db),
                           GRAPH3=make_graph('line', 'graph3', [i for i in range(11)],
                                             "TITLE", [randint(0, 100) for _ in range(11)], True),
                           MENU=make_menu(db))


@app.route('/course/<course>')
def course_page(course: str):
    db = "scripts/DataBase/inginious.sqlite"
    course = request(db, "SELECT DISTINCT(course) FROM user_tasks WHERE course LIKE \"{0}%\"".format(course))[0][0]
    req_fail = "SELECT DISTINCT(task), COUNT(result) FROM submissions WHERE course='{0}' GROUP BY task".format(course)
    req_success = "SELECT DISTINCT(task), COUNT(result) FROM submissions " \
                  "WHERE course='{0}'  AND result='success' GROUP BY task".format(course)
    return render_template("base.html", STYLE=url_for('static', filename="base.css"), MENU=make_menu(db),
                           GRAPH3=double_bar_graph(db, req_fail, req_success))


@app.route('/course/<course>/<task>')
def task_page(course: str, task: str):
    db = "scripts/DataBase/inginious.sqlite"
    return render_template("base.html", STYLE=url_for('static', filename="base.css"), MENU=make_menu(db),
                           GRAPH1=student_perform_graph(db, task))
