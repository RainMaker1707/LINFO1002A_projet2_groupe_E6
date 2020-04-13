from flask import Flask, render_template, url_for
from scripts.courseList import *
from scripts.actualitiesGraph import *
app = Flask(__name__, template_folder='templates', static_folder='style')


@app.route('/')
def home():
    """
    :return:
    """
    db = "scripts/Database/inginious.sqlite"
    return render_template("base.html",
                           STYLE=url_for('static', filename="base.css"),
                           GRAPH1=make_graph("bar", "main_graph", ['a', 'b', 'c', 'd'], "time", [10, 12, 15, 12], True),
                           GRAPH2=make_graph("doughnut", "main_graph2", ['a', 'b', 'c'], "time", [10, 12, 30], True),
                           MENU=courses_list_templating(db))
