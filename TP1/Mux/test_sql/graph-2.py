import sqlite3
from fcts import read_file,write_file

def get_entries(task):
	"""
	return list of entries
	[(/entry/),(course,task,date,username,result)]
	"""

	lst = []
	c = sqlite3.connect('inginious.sqlite').cursor()
		
	for row in c.execute("SELECT task, username, result from submissions ORDER BY submitted_on ASC"):
		if row[0] == task:
			lst.append(row)

	return lst

def get_values(task):
	temp = get_entries(task)
	users_results = {}
	data = [0,0,0,0]

	for entry in temp:
		if entry[1] not in users_results:
			users_results[entry[1]] = entry[2]
			if entry[2] == 'success':
				data[1] += 1

		elif users_results[entry[1]] == 'failed':
			users_results[entry[1]] = entry[2]

	print(users_results)
	for i in users_results.items():
		if i[1] == 'success':
			data[0] += 1
		elif i[1] == 'failed':
			data[2] += 1
		else:
			data[3] += 1
	print(data)
	return data


def graph_2(task):
	"""
	return the js script for the graph 1 of the given task
	"""
	data = get_values(task)
	dataset = "{"+'label: "{1}",\n backgroundColor: ["rgba(0,200,0,0.8)","rgba(0,255,0,0.8)","rgba(255,0,0,0.8)"],\n data: {0},\n'.format(data,task)+"}"

	#create and save the sript
	script = read_file("template2.html")
	script = script.replace("#data#",dataset)
	script = script.replace("#labels#",str(["pass","first_try","fail","error"]))

	write_file("out.html",script)
	return script


graph_2("intersection")