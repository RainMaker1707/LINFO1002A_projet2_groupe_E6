from flask import Flask
from TP1.OldTry.PageCreator import *

app = Flask(__name__)


@app.route('/')
@app.route('/base.html')
def home():
    """
    Home page from the site
    :return:
    """
    content_str = read_file("Html/base.html")
    content_str = make_menu(content_str)
    content_str = make_title(content_str)
    return content_str.replace('X', "<body><u>CHECK HOMEPAGE</u></body>")


@app.route('/CSS/home.css')
def home_style():
    return read_file("CSS/home.css")


@app.route("/graph.html")
def graph():
    """
    :return: Graph page test for an interactive graph
    """
    content_str = read_file("Html/graph.html")
    content_str = make_title(content_str)
    content_str = make_menu(content_str)
    return content_str.replace('X', "<body><u>CHECK GRAPH PAGE</u></body>")


@app.route('/CSS/graph.css')
def graph_style():
    return read_file("CSS/graph.css")


@app.route('/coursesList.html')
def courses():
    """
    :return:
    """
    content = make_menu(read_file("Html/coursesList.html"))

    return make_title(content)


@app.route('/CSS/coursesList.css')
def courses_style():
    return read_file("CSS/coursesList.css")
