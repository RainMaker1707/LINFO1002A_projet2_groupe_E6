def get_data(path_file):
    """
    :param path_file: string path to file .csv which content all datas
    :return: a matrix which contains line of files
    """
    try:
        with open(path_file, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        with open(path_file, 'w') as file:
            file.close()
        return get_data(path_file)

def get_script(path):
    """
    return one string with the entire file
    """
    content_str = ""
    try:
        with open(path, 'r') as file:
            for line in file:
                content_str += line
    except:
        pass
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
                ret_lst[i].append(temp_str)
                temp_str = ""
            else:
                temp_str += heavy_str_data[i][j]
    return ret_lst

script = get_script("maxime.html")
data = format_data(get_data("total_cases.csv"))

"{label:'Stock A', fill: false, borderColor: 'red', data: [65, 59, 80, 81, 56, 55, 40, ,60,55,30,78], spanGaps: true,}"


script = script.replace("#data#",)
script = script.replace("#label#",)
