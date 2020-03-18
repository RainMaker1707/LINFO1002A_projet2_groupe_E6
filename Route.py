from flask import Flask
from PageCreator import *

app = Flask(__name__)


@app.route('/')
def home():
    """
    Home page from the site
    :return:
    """
    content_str = read_file("Html/home.html")
    content_str = make_style(content_str, "CSS/home.css")
    content_str = make_menu(content_str)
    content_str = make_title(content_str)
    return content_str.replace('X', "<body><u>CHECK HOMEPAGE</u></body>")


@app.route("/graph.html")
def graph():
    """
    :return: Graph page test for an interactive graph
    """
    content_str = read_file("Html/graph.html")
    content_str = make_style(content_str)
    content_str = make_title(content_str)
    content_str = make_menu(content_str)
    return content_str.replace('X', "<body><u>CHECK GRAPH PAGE</u></body>")
