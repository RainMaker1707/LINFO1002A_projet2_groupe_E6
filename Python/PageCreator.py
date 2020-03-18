from flask import Flask
app = Flask(__name__)


def read_file(path):
    content_str = str()
    with open(path, 'r') as file:
        for line in file:
            content_str += line
    return content_str


def make_style(html_content, css_file=None):
    """
    :param html_content: string content of the html file
    :param css_file:
    :return: and HTML string to config the style sheet
    """
    if css_file is None:
        return html_content.replace("STYLE_LINK", " ")
    else:
        return html_content.replace("STYLE_LINK", "<link href={0} ref=stylesheet>".format(css_file))


def make_menu(html_content):
    """
    :param html_content: string content of the html file
    :return:
    """
    return html_content.replace("MENU", "<ul><li><a href=\"graph.html\">Graph</a></li></ul>")


def make_title(html_content):
    """
    :param html_content:
    :return: an HTML string to config the title of the slide in the nav board
    """
    return html_content.replace("TITLE", "<title>Coronavirus CoViD-19 propagation</title>")


@app.route('/')
def home():
    content_str = read_file("Html/home.html")
    content_str = make_style(content_str, "CSS/home.css")
    content_str = make_menu(content_str)
    content_str = make_title(content_str)
    return content_str.replace('X', "<body><u>CHECK HOMEPAGE</u></body>")


@app.route("/graph.html")
def graph():
    content_str = read_file("Html/graph.html")
    content_str = make_style(content_str)
    content_str = make_title(content_str)
    content_str = make_menu(content_str)
    return content_str.replace('X', "<body><u>CHECK GRAPH PAGE</u></body>")
