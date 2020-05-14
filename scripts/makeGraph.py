from scripts.functions import *


def make_graph(graph_type: str, graph_id: str, labels: list, title, data: list,
               options=None, color_lst=None, legend=None, hide_datasets=None):
    """
    Function which return a canvas with the chart.js script set with the following data
    :param graph_type: type of the graph ( bar, line, doughnut, pie, etc)
    :param graph_id: canvas id to link the css part of base.css to the graph container
    :param labels: list of the labels on the X axes for the typical graph or name of part in doughnut/pie graph
    :param title: string, title of the graph
    :param data: list of y value or part of pie/doughnut, list of list if multiple dataset
    :param color_lst: list of color you want in the graph, list of list if multiple dataset
           pattern : ["rgba(r: int, g: int, b: int, a: float(0,1)",...,"rgba(r: int, g: int, b: int, a: float(0,1)"]
           if not given colors are chosen randomly
    :param legend: string or list on dataset label
    :param options: options you want to set in
    :param hide_dataset: list of dataset index to hide on load
    :return: the string part of the html code to plain the template
    """
    canvas = "<canvas id=\"{0}\">\n<script>\nvar ctx = document.getElementById('{0}')".format(graph_id)
    canvas += ".getContext('2d');\n"
    canvas += "var myChart = new Chart(ctx, {\n"
    canvas += "type:'{0}',\ndata: #1\nlabels: {1},\ndatasets: [#1".format(graph_type, labels)

    if legend:
        if isinstance(legend, str):
            tmp = list()
            tmp.append(legend)
            legend = tmp

    if not isinstance(data[0], list):
        tmp = list()
        tmp.append(data)
        data = tmp
        if legend:
            if len(data) != len(legend):
                return "the number of dataset does not match between data and legend"
                
    if color_lst:
        if not isinstance(color_lst[0], list) and graph_type != "line":
            tmp = list()
            tmp.append(color_lst)
            color_lst = tmp

    # add dataset
    for i in range(len(data)):
        # label
        if legend:
            canvas += "\n\tlabel: '{0}',\n".format(legend[i])
        # hide
        if hide_dataset:
            if i in hide_dataset:
                canvas += "\thidden: true,\n"

        # colors
        if color_lst:
            canvas += "\tfill: true,\n\tbackgroundColor : {0},\n".format(color_lst[i])
        else:
            canvas += "\tfill : true,\n\tbackgroundColor: [\n\t\t"
            if graph_type == "line" or graph_type == "radar":
                lst = get_random_colors(1)
                for _ in range(len(data[i])):
                    canvas += "\"rgba{0}\",\n\t\t".format(lst[0])
            else:
                lst = get_random_colors(len(labels))
                for j in range(len(lst)):
                    canvas += "\"rgba{0}\",\n\t\t".format(lst[j])
            canvas += "],\n\t"
        # data
        canvas += "data: {0}\n".format(data[i])
        if i < len(data)-1:
            canvas += "\t\t}, {\n"

    canvas += "#2]\n#2,\n"

    if options:
        canvas += "options: #1\ntitle: #1\ndisplay: true,\nfontSize: 20,\n text: '{0}'\n#2,\nlegend: #1 position: " \
                  "'bottom'#2, {1}\n#2\n".format(title, options)
    else:
        canvas += "options: #1\ntitle: #1\ndisplay: true,\nfontSize: 20,\ntext: '{0}'\n#2,\nlegend: " \
                  "#1 position: 'bottom'#2#2\n".format(title)
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
    chart += "backgroundColor: \"rgba(230,0,0,0.8)\",\n\t\t"
    chart += "data: {0},\n\t\t".format(y_axe)
    chart += "},{\n\t\t"
    chart += "label: 'success',\n\t\t"
    chart += "backgroundColor: \"rgba(0,200,0,0.8)\",\n\t\t"
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
    return make_graph('pie', 'total_sub', x_axe, "Total submissions", y_axe, color_lst=get_colors(len(y_axe)))


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
        return ""

    lst = ["success", "failed", "errors"]
    return make_graph("pie", "subs_rep", lst, "Distribution of all submissions result", data,
                      color_lst=['rgba(0, 200, 0, 0.85)', 'rgba(230, 0, 0, 0.85)', 'rgba(255, 115, 0, 0.85)'])


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
        return ""

    lst = ["success", "failed", "error", "first try"]
    return make_graph("doughnut", "subs_rep2", lst, "Distribution of best performance by student", data,
                      color_lst=get_colors(4))


def graph_submissions_distribution(filename: str, task: str):
    """
    :param filename:
    :param task:
    :return:
    """
    dates = dict()
    days_lst = list()
    data = request(filename, "SELECT task, submitted_on, result from submissions WHERE task='{0}' "
                             "ORDER BY submitted_on".format(task))
    if not data:
        return "<p style=\"color: #E99002\">It appears, we have no submissions " \
               "for this task: {0}.</p>".format(task)

    for entry in data:
        days_lst.append((date_format(entry[1]), entry[2]))
        dates[entry[1][0:10].replace("-", "/")] = None

    dates_lst = date_dic_to_list(dates, days_lst[-1][0]-days_lst[0][0], days_lst[0][0])
    values = [0 for _ in range(len(dates_lst))]
    values_success = [0 for _ in range(len(dates_lst))]
    values_error = [0 for _ in range(len(dates_lst))]

    for date in days_lst:
        values[date[0]-days_lst[0][0]-1] += 1
        if date[1] == "success":
            values_success[date[0] - days_lst[0][0] - 1] += 1
        elif date[1] != "failed":
            values_error[date[0]-days_lst[0][0]-1] += 1

    tmp = get_colors(3)
    colors = list()
    for i in reversed(tmp):
        colors.append("\""+i+"\"")

    return make_graph("line", "subs_rep3", dates_lst, "Evolution of submissions over the task duration",
                      [values, values_success, values_error], legend=["submissions", "success", "errors"],
                      color_lst=colors, hide_dataset=[2])


def inter_fun_y_axe(top_list):
    """
    :param top_list:
    :return:
    """
    top_list.reverse()
    x_axe = [0 for _ in range(len(top_list))]
    length = len(top_list)
    lst = []
    for i in range(len(top_list)):
        if i % 2 == 0:
            x_axe[int(i / 2)] = top_list[i]
        else:
            x_axe[- int(i / 2 + 0.5)] = top_list[i]
        if i > 0 and top_list[i][0] == top_list[i - 1][0]:
            length -= 1
        else:
            lst.append(top_list[i][0])
    lst.reverse()
    return x_axe, length, lst


def top_subs_count(filename: str, top_size: int, graph_type: str, req: str, title: str,
                   graph_id: str, mirrored=False):
    """
    :param filename:
    :param top_size:
    :param graph_type:
    :param graph_id:
    :param req: the sql request of 2 or 3 elements
    :param title: the title of the graph on the page
    :param mirrored: True = top worst, False = top best
    """
    data_list = request(filename, req)
    if mirrored:
        data_list.sort(reverse=True)
    else:
        data_list.sort()
   
    data_list = data_list[0:top_size]
    data = []
    titles = []
    for entry in data_list:
        data.append(entry[0])
        if len(entry) > 2:
            titles.append(entry[2]+" ("+entry[1]+")")
        else:
            titles.append(entry[1])

    if mirrored:
        colors = get_colors(len(data))
    else:
        colors = get_colors(len(data))
        colors.reverse()

    return make_graph(graph_type, graph_id, titles, title, data, legend="submissions count",
                      options="scales: #1 xAxes: [#1display: true#2], yAxes: [#1display: "
                              "false#2]#2".replace("#1", "{").replace("#2", "}"), color_lst=colors)


def graph_error_distribution(filename: str, task: str):
    total = request(filename, "SELECT COUNT(result) FROM submissions WHERE task=\"{0}\"".format(task))[0][0]
    if total == 0:
        return ""
    temp = request(filename, "SELECT result FROM submissions GROUP BY result")
    labels = list()
    for i in temp:
        if i[0] is not None and i[0] != "success" and i[0] != "failed":
            labels.append(i[0])
    data = list()
    for i in labels:
        data.append(request(filename, "SELECT COUNT(result) FROM submissions WHERE result=\"{0}\" "
                                      "AND task LIKE \"%{1}%\"".format(i, task[:4]))[0][0])

    return make_graph("radar", "error_distribution", labels, "Distribution of all errors for the task", data,
                      options="legend: {display: false}")


def graph_week_distribution(filename: str, course: str):
    subs = request(filename, "SELECT submitted_on FROM submissions WHERE course=\"{0}\"".format(course))
    data = [0.0 for _ in range(7)]
    tot = 0

    for date in subs:
        data[find_day(date[0][:10])] += 1
        tot += 1

    for i in range(len(data)):
        data[i] = int((data[i]/tot) * 10000) / 100

    return make_graph("bar", "week_distribution", ["Monday", "Tuseday", "Wednesday", "Thursday", "Friday", "Saturday",
                      "Sunday"], "typical week activity distribution", data,
                      color_lst=get_colors(7),
                      options="scales: {yAxes: [{ticks: {suggestedMin: 0, suggestedMax: 50}}]},"
                              "legend: {display: false}")


def graph_day_distribution(filename: str, course: str):
    subs = request(filename, "SELECT submitted_on FROM submissions WHERE course=\"{0}\"".format(course))
    data = [0.0 for _ in range(24)]
    tot = 0

    for date in subs:
        data[int(date[0][11:13])-1] += 1
        tot += 1

    for i in range(len(data)):
        data[i] = int((data[i] / tot) * 10000) / 100

    return make_graph("bar", "day_distribution", [i for i in range(1, 25)],
                      "typical day activity distribution", data, color_lst=get_colors(24),
                      options="scales: {yAxes: [{ticks: {suggestedMin: 0, suggestedMax: "
                              "50}}]},legend: {display: false}")
