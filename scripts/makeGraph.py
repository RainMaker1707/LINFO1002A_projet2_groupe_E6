from random import randint
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
        lst.append(row)
    connection.close()
    return lst


def format_request_where(req: str, where_arg: str):
    """
    :param req: SQL request to format
    :param where_arg: arg to set at WHERE="where_arg"
    :return: str: a clean SQL request with set WHERE
    """
    return req.replace("WHERE ", "WHERE {0}".format(where_arg))


def get_random_colors(number: int):
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
            lst = get_random_colors(1)
            for i in range(len(data)):
                canvas += "\"rgba{0}\",\n\t\t".format(lst[0])
        else:
            lst = get_random_colors(len(labels))
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


def double_bar_graph(filename: str, req_fail: str, req_success: str):
    """
    :param filename: data base file path
    :param req_fail: SQL req to select the fail submissions
    :param req_success: SQL req to select the success submissions
    :return: str : a double bar graph ofr each course with all submissions / success for each course
    """
    sub_lst = request(filename, req_fail)
    success_lst = request(filename, req_success)
    x_axe, y_axe, y_axe_2 = list(), list(), list()
    for i in range(len(success_lst)):
        x_axe.append(sub_lst[i][0])
        y_axe.append(sub_lst[i][1])
        y_axe_2.append(success_lst[i][1])
    chart = "<canvas id='double_bar'><script>\n"
    chart += "var ctx = document.getElementById('double_bar').getContext('2d');\n"
    chart += "var data = {\n\t"
    chart += "labels: {0},\n\t".format(x_axe)
    chart += "datasets: [{\n\t\t"
    chart += "label: 'attempt',\n\t\t"
    chart += "backgroundColor: 'red',\n\t\t"
    chart += "data: {0},\n\t\t".format(y_axe)
    chart += "},{\n\t\t"
    chart += "label: 'success',\n\t\t"
    chart += "backgroundColor: 'lime',\n\t\t"
    chart += "data: {0},\n\t\t".format(y_axe_2)
    chart += "}]};\n"

    chart += "var myBarChart = new Chart(ctx, {\n\ttype: 'bar',\n\tdata: data,\n\toptions: {\n\t\t"
    chart += "barValueSpacing: 20,\n\t\tscales:{\n\t\t\tyAxes: [{\n\t\t\t\tticks: { min: 0}\n\t\t\t}]\n\t\t}\n\t}\n});"
    chart += "\n</script></canvas>\n"
    return chart


def graph_total_sub(filename: str):
    """
    :param filename: data base file path
    :return: str: a pie graph with the total submissions per courses in de data base
    """
    lst = request(filename, "SELECT course,COUNT(submission)FROM user_tasks GROUP BY course")
    x_axe, y_axe = list(), list()
    for i in range(len(lst)):
        if len(lst[i][0]) > 10:
            for j in range(len(lst[i][0])):
                if lst[i][0][j] == '-':
                    x_axe.append(lst[i][0][:j])
        else:
            x_axe.append(lst[i][0])
        y_axe.append(lst[i][1])
    return make_graph('pie', 'total_sub', x_axe, "Total submissions", y_axe, True)
