from flask import Flask, render_template, url_for
from scripts.courseList import *
app = Flask(__name__, template_folder='templates', static_folder='style')


@app.route('/')
def home():
    """
    :return:
    """
    db = "scripts/Database/inginious.sqlite"
    return render_template("base.html",
                           STYLE=url_for('static', filename="base.css"),
                           MENU=courses_list_templating(db))
