def get_data(path_file):
    """
    :param path_file: string path to file .csv which content all datas
    :return: a list which contains line of files
    """
    try:
        with open(path_file, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        with open(path_file, 'w') as file:
            file.close()
        return get_data(path_file)


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
                ret_lst[i].append(temp_str)
                temp_str = ""
            else:
                temp_str += heavy_str_data[i][j]
    return ret_lst


def get_europa(clean_data, date):
    """
    :param clean_data: data from format_data()
    :param date: given date iso format, string type, to search in matrix_data
    :return: a matrix with the twelve first europa land and cases in given date
    """
    europa = [[], []]
    lands = ["Austria", "Belgium", "France", "Germany", "Greece", "Iceland", "Italy", "Luxembourg", "Spain", "Finland",
             "Netherlands", "Portugal"]
    case_list = []
    for k in range(1, len(clean_data)):
        if clean_data[k][0] == date:
            case_list = clean_data[k]
    for i in range(len(clean_data[0])):
        if clean_data[0][i] in lands:
            europa[0].append(clean_data[0][i])
            europa[1].append(case_list[i])
    return europa
