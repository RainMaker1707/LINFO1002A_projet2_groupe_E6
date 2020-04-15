from scripts.functions import *


def make_graph(graph_type: str, graph_id: str, labels: list, title: str, data: list, fill_random=False,
               options: str = None, fixed=False, color_lst=None):
    """
    Function which return a canvas with the chart.js script set with the following datas
    :param graph_type: type of the graph ( bar, line, doughnut, pie, etc)
    :param graph_id: canvas id to link the css part of base.css to the graph container
    :param labels: list of the labels on the X axes for the typical graph or name of part in doughnut/pie graph
    :param title: title of the graph when is axes graph
    :param data: data for y axe graph or part of pie/doughnut
    :param fill_random: to fill with random color
    :param fixed: if you want fixed colors you have to pass a list of these color in arg a nd set fixed at True
    :param color_lst: list of color you want in the graph
    :param options: options you want to set in
    :return: the string part of the html code to plain the template
    """
    # if len(data) != len(labels):
    #    return "ERROR data and labels must have the same len\n"

    canvas = "<canvas id=\"{0}\">\n<script>\nvar ctx = document.getElementById('{0}')".format(graph_id)
    canvas += ".getContext('2d');\n"
    canvas += "var myChart = new Chart(ctx, {\n"
    canvas += "type:'{0}',\ndata: #1\nlabels: {1},\ndatasets: [#1\n\tlabel: '{2}',\n".format(graph_type, labels, title)
    if fixed and color_lst:
        canvas += "\tfill: true,\n\tbackgroundColor : {0},\n".format(color_lst)
    elif fill_random:
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


def student_perform_graph(filename: str, task: str):
    """
    :param filename:
    :param task:
    :return:
    """
    entries = request(filename, "SELECT task, username, result FROM submissions WHERE task='{0}'"
                                "ORDER BY submitted_on ASC".format(task))
    data = [0, 0, 0]
    for entry in entries:
        if entry[2] == 'success':
            data[0] += 1
        elif entry[2] == 'failed':
            data[1] += 1
        else:
            data[2] += 1
    if data == [0, 0, 0]:
        return "it apears, we have no submissions for this task."

    lst = ["success", "failed", "error"]
    return make_graph("pie", "subs_rep", lst, "repartition of best performance by student", data,
                      fixed=True, color_lst=['lime', 'red', 'orange'])


def best_user_perf(filename: str, task: str):
    """
    :param filename:
    :param task:
    :return:
    """
    entries = request(filename, "SELECT task, username, result FROM submissions WHERE task='{0}'"
                                " ORDER BY submitted_on ASC".format(task))
    users_results = {}
    data = [0, 0, 0, 0]
    for entry in entries:
        if entry[1] not in users_results:
            users_results[entry[1]] = entry[2]
            if entry[2] == 'success':
                data[3] += 1
        elif users_results[entry[1]] == 'failed':
            users_results[entry[1]] = entry[2]
    for result in users_results.items():
        if result[1] == 'success':
            data[0] += 1
        elif result[1] == 'failed':
            data[1] += 1
        else:
            data[2] += 1
    data[0] -= data[3]
    if data == [0, 0, 0, 0]:
        return "it apears, we have no submissions for this task."

    lst = ["success", "failed", "error", "first try"]
    return make_graph("doughnut", "subs_rep2", lst, "repartition of all submissions result", data, fill_random=True)


def graph_submissions_repartition(filename: str, task: str):
    """
    :param filename:
    :param task:
    :retun:
    """
    dates = dict()
    days_lst = list()
    data = request(filename, "SELECT task, submitted_on from submissions WHERE task='{0}' ORDER BY submitted_on".format(task))
    if data == []:
        return "It appears, we have no submissions for this task: {0}.".format(task)

    for entry in data:
        days_lst.append(date_format(entry[1]))
        dates[entry[1][0:10].replace("-", "/")] = None
    days_lst.sort()
    dates_lst = date_dic_to_list(dates, days_lst[-1]-days_lst[0], days_lst[0])
    values = [0 for _ in range(len(dates_lst))]
    for date in days_lst:
        values[date-days_lst[0]-1] += 1
    return make_graph("line", "subs_rep3", dates_lst, "Evolution of submissions over the task duration", values, True)
