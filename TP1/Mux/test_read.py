def get_data(path_file):
    """
    :param path_file: string path to file .csv which content all datas
    :return: a matrix which contains line of files
    """
    try:
        with open(path_file, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        return False


def get_script(path):
    """
    return one string with the entire file
    """
    content_str = ""
    try:
        with open(path, 'r') as file_in:
            for line in file_in:
                content_str += line
    except FileNotFoundError:
        return -1
    return content_str


def format_data(heavy_str_data):
    """
    :param heavy_str_data: list of a string per line in .csv file
    :return: a clean matrix of string list per line
    """
    ret_lst = [[] for _ in range(len(heavy_str_data))]
    for i in range(len(heavy_str_data)):
        temp_str = ""
        for j in range(len(heavy_str_data[i])):
            if heavy_str_data[i][j] == ',':
                if temp_str == "":
                    ret_lst[i].append(0)
                else:
                    try:
                        ret_lst[i].append(int(temp_str))
                        temp_str = ""
                    except ValueError:
                        ret_lst[i].append(temp_str)
                        temp_str = ""
            else:
                temp_str += heavy_str_data[i][j]
    return ret_lst


def reverse(matrix):
    ret = [[] for _ in range(len(matrix[0]))]
    for i in range(len(matrix[0])):
        temp = []
        for j in range(len(matrix)):
            temp.append(matrix[j][i])
            ret[i] = temp
    return ret


def main():
    script = get_script("maxime.html")
    data = reverse(format_data(get_data("total_cases.csv")))
    #  Js string : "{label: {0}, fill: false, borderColor: 'red', data: {1}, spanGaps: true}"
    dates = data[0][1:]
    dataset = ""
    for j, i in enumerate(data[1:]):
        dataset += "{"+'label: "{0}",\n fill: false,\n borderColor: "red",\n data: {1},\n spanGaps: true,\n'.\
            format(i[0], i[1:])+"}"
        if j < len(data)-1:
            dataset += ", "

    script = script.replace("#data#", dataset)
    script = script.replace("#labels#", str(dates))

    with open("out.html", 'w') as file:
        file.write(script)
    return


main()
