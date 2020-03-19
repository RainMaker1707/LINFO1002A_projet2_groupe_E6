def read_file(path):
    """
    :param path: string path to the file html
    :return:  the string content of the file
    """
    content_str = str()
    with open(path, 'r') as file:
        for line in file:
            content_str += line
    return content_str


def make_menu(html_content):
    """
    :param html_content: string content of the html file
    :return:
    """
    menu = ""
    menu += "<ul id=\"menu\">"  # menu start
    menu += "<li><a href=\"home.html\">Home</a></li>"
    menu += "<li><a href=\"graph.html\">Graph</a></li>"
    menu += "<li><a href=\"coursesList.html\">Courses</a></li>"
    menu += "</ul>"  # menu end
    print(menu)
    return html_content.replace("MENU", menu)


def make_title(html_content):
    """
    :param html_content:
    :return: an HTML string to config the title of the slide in the nav board
    """
    return html_content.replace("TITLE", "<title> Inginious submission stats</title>")
