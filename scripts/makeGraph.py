from random import randint, random
import sqlite3


def request(filename: str, req: str):
    """
    :param filename: filename of the data base
    :param req: SQL request to send to bdd
    :return: a list of the tuple gave from SQL request
    """
    connection = sqlite3.connect(filename).cursor()
    lst = list()
    for row in connection.execute(req):
        lst.append(row[0])
    connection.close()
    return lst


def get_random_color(number: int):
    """
    :param number: number of tuple
    :return: a list of tuple of color in rgba : (r(0, 250), g(0, 250), b(0, 250), a(0, 1))
    """
    lst = list()
    for i in range(number):
        lst.append((randint(0, 250), randint(0, 250), randint(0, 250), 0.8))
    return lst


def make_graph(graph_type: str, graph_id: str, labels: list, title: str, data: list, fill=False, options: str = None):
    """
    Function which return a canvas with the chart.js script set with the following datas
    :param graph_type: type of the graph ( bar, line, doughnut, pie, etc)
    :param graph_id: canvas id to link the css part of base.css to the graph container
    :param labels: list of the labels on the X axes for the typical graph or name of part in doughnut/pie graph
    :param title: title of the graph when is axes graph
    :param data: data for y axe graph or part of pie/doughnut
    :param fill: to fill with random color
    :param options: options you want to set in
    :return: the string part of the html code to plain the template
    """
    if len(data) != len(labels):
        return "ERROR data and labels must have the same len\n"

    canvas = "<canvas id=\"{0}\">\n<script>\nvar ctx = document.getElementById('{0}')".format(graph_id)
    canvas += ".getContext('2d');\n"
    canvas += "var myChart = new Chart(ctx, {\n"
    canvas += "type:'{0}',\ndata: #1\nlabels: {1},\ndatasets: [#1\n\tlabel: '{2}',\n".format(graph_type, labels, title)
    if fill:
        canvas += "\tfill : true,\n\tbackgroundColor: [\n\t\t"

        if graph_type == "line":
            lst = get_random_color(1)
            for i in range(len(data)):
                canvas += "\"rgba{0}\",\n\t\t".format(lst[0])
        else:
            lst = get_random_color(len(labels))
            for i in range(len(lst)):
                canvas += "\"rgba{0}\",\n\t\t".format(lst[i])
        canvas += "],\n\t"
    canvas += "data: {0}\n#2]\n#2,\n".format(data)
    if options:
        canvas += "options: #1\n{0}\n#2\n".format(options)
    canvas += "#2);\n</script>\n</canvas>"
    canvas = canvas.replace('#1', '{')
    canvas = canvas.replace('#2', '}')
    return canvas
