from scripts.functions import *


def make_graph(graph_type: str, graph_id: str, labels: list, title: str, data: list, fill_random=False,
               options: str = None, fixed=False, color_lst=None):
    """
    Function which return a canvas with the chart.js script set with the following data
    :param graph_type: type of the graph ( bar, line, doughnut, pie, etc)
    :param graph_id: canvas id to link the css part of base.css to the graph container
    :param labels: list of the labels on the X axes for the typical graph or name of part in doughnut/pie graph
    :param title: title of the graph when is axes graph
    :param data: data for y axe graph or part of pie/doughnut
    :param fill_random: to fill with random color
    :param fixed: if you want fixed colors you have to pass a list of these color in arg a nd set fixed at True
    :param color_lst: list of color you want in the graph
           pattern : ["rgba(r: int, g: int, b: int, a: float(0,1)",...,"rgba(r: int, g: int, b: int, a: float(0,1)"]
    :param options: options you want to set in
    :return: the string part of the html code to plain the template
    """
    canvas = "<canvas id=\"{0}\">\n<script>\nvar ctx = document.getElementById('{0}')".format(graph_id)
    canvas += ".getContext('2d');\n"

    #rainbow gradiant
    canvas += "var gradientStroke = ctx.createLinearGradient(0, 0, 2000, 0);\n"
    canvas += "gradientStroke.addColorStop(0, \'rgba(255, 0, 0, 0.6)\');\ngradientStroke.addColorStop(0.16, \'rgba(255, 255, 0, 0.6)\');\n"
    canvas += "gradientStroke.addColorStop(0.32, \'rgba(0, 255, 0, 0.6)\');\ngradientStroke.addColorStop(0.5, \'rgba(0, 255, 255, 0.6)\');\n"
    canvas += "gradientStroke.addColorStop(0.66, \'rgba(0, 0, 255, 0.6)\');\ngradientStroke.addColorStop(0.82, \'rgba(255, 0, 255, 0.6)\');\n"
    canvas += "gradientStroke.addColorStop(1, \'rgba(255, 0, 0, 0.6)\');\n"

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
    else:
        canvas += "\tfill: true,\n\tbackgroundColor : gradientStroke,\n"

    canvas += "data: {0}\n#2]\n#2,\n".format(data)
    if options:
        canvas += "options: #1\ntitle: #1\ndisplay: true,\n text: '{0}'\n#2,\nlegend: #1 position: 'bottom'#2," \
                  " {1}\n#2\n".format(title, options)
    else:
        canvas += "options: #1\ntitle: #1\ndisplay: true,\n text: '{0}'\n#2,\nlegend: #1 position: 'bottom'" \
                  "#2#2\n".format(title)
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
    chart += "backgroundColor: \"rgba(255,0,0,0.8)\",\n\t\t"
    chart += "data: {0},\n\t\t".format(y_axe)
    chart += "},{\n\t\t"
    chart += "label: 'success',\n\t\t"
    chart += "backgroundColor: \"rgba(0,255,0,0.8)\",\n\t\t"
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
        return ""

    lst = ["success", "failed", "error"]
    return make_graph("pie", "subs_rep", lst, "repartition of best performance by student", data,
                      fixed=True, color_lst=['rgba(0, 255, 0, 0.85)', 'rgba(255, 0, 0, 0.85)', 'rgba(255, 115, 0, 0.85)'])


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
    return make_graph("doughnut", "subs_rep2", lst, "repartition of all submissions result", data, fill_random=True)


def graph_submissions_repartition(filename: str, task: str):
    """
    :param filename:
    :param task:
    :retun:
    """
    dates = dict()
    days_lst = list()
    data = request(filename, "SELECT task, submitted_on from submissions WHERE task='{0}' "
                             "ORDER BY submitted_on".format(task))
    if not data:
        return "<p style=\"color: #E99002\">It appears, we have no submissions " \
               "for this task: {0}.</p>".format(task)

    for entry in data:
        days_lst.append(date_format(entry[1]))
        dates[entry[1][0:10].replace("-", "/")] = None
    days_lst.sort()
    dates_lst = date_dic_to_list(dates, days_lst[-1]-days_lst[0], days_lst[0])
    values = [0 for _ in range(len(dates_lst))]
    for date in days_lst:
        values[date-days_lst[0]-1] += 1
    return make_graph("line", "subs_rep3", dates_lst, "Evolution of submissions over the task duration", values, True)


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


def top_subs_count(filename: str, top_size: int, graph_type: str, req: str, title: str, graph_id: str, mirrored=False, podium=False):
    """
    :param filename:
    :param top_size:
    :param graph_type:
    :param graph_id:
    :param req: the sql request of 2 or 3 elements
    :param title: the title of the graph on the page
    :param mirrored: True = top worst, False = top best
    :return:
    """
    datas = request(filename, req)
    if mirrored:
        datas.sort(reverse=True)
    else:
        datas.sort()
    if podium == True:
        lst, length, scores = inter_fun_y_axe(datas[0:top_size])

        data = []
        titles = []
        user: tuple
        for user in lst:
            for poss, score in enumerate(scores):
                if score == user[0]:
                    data.append(1 - poss/1000)
                    break
            if len(user) > 2:
                titles.append(user[2]+" "+user[1]+" "+str(user[0]))
            else:
                titles.append(user[1]+" "+str(user[0]))

    else:
        datas = datas[0:top_size]
        data = []
        titles = []
        for entry in datas:
            data.append(entry[0])
            if len(entry) > 2:
                titles.append(entry[1]+" "+entry[2])
            else:
                titles.append(entry[1])

    return make_graph(graph_type, graph_id, titles, title, data, True,
                      options="scales: { xAxes: [{display: true}], yAxes: [{display: false}]}")
