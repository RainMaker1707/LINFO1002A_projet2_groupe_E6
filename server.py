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
                           GRAPH1=make_graph("bar", "main_graph", ['a', 'b', 'c', 'd'], "time", [10, 12, 15, 12], True,
                                             "scales: {yAxes: [{ticks: {beginAtZero:true}}]}"),
                           GRAPH2=graph_total_sub(db),
                           GRAPH3=make_graph('line', 'graph3', [i for i in range(10)],
                                             "TITLE",[randint(0, 100) for _ in range(10)], True),
                           MENU=courses_list_templating(db))
