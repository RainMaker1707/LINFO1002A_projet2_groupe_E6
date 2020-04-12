from random import randint
from flask import Flask
app = Flask(__name__)

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
        replace every gap by zero
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
	            	except:
	            		ret_lst[i].append(temp_str)
	            		temp_str = ""
            else:
                temp_str += heavy_str_data[i][j]
    return ret_lst

def reverse(matrix):
    """
    turn matrix 90 degrees
    """
    ret = [[] for _ in range(len(matrix[0]))]
    for i in range(len(matrix[0])):
        temp = []
        for j in range(len(matrix)):
            temp.append(matrix[j][i])
            ret[i] = temp
    return ret

def write_file(path,text):
    """
    path = string
    text = string

    write the string to the file in the path
    """
    with open(path, 'w') as file:
        file.write(text)

def get_color():
    """
    return a tuple of three + 1
    the ints are between 0 and 255
    """
    return (randint(50,255),randint(50,255),randint(50,255),0.6)

@app.route('/')
def main():
    data = reverse(format_data(get_data("total_deaths.csv")))
    print(data)
    dates = data[0][1:]
    datasets = ""

    for j,i in enumerate(data[1:]):
        datasets += "{"+'label: "{0}",\n fill: false,\n borderColor: "rgba{2}",\n data: {1},\n spanGaps: true,\n'.format(i[0],i[1:],str(get_color()))+"}"
        if j < len(data)-1:
            datasets += ", "

    #create and save the sript
    script = get_script("template.html")
    script = script.replace("#data#",datasets)
    script = script.replace("#labels#",str(dates))

    write_file("out.html",script)
    return script

main()