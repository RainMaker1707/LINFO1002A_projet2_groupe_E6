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
	c.close()

	return lst

def get_values(task):
	temp = get_entries(task)
	users_results = {}
	data = [0,0,0,0]
	data2 = [0,0,0]

	for entry in temp:
		#first dataset
		if entry[1] not in users_results:
			users_results[entry[1]] = entry[2]
			if entry[2] == 'success':
				data[3] += 1

		elif users_results[entry[1]] == 'failed':
			users_results[entry[1]] = entry[2]

		#second dataset
		if entry[2] == 'success':
			data2[0] += 1
		elif entry[2] == 'failed':
			data2[1] += 1
		else:
			data2[2] += 1

	for i in users_results.items():
		if i[1] == 'success':
			data[0] += 1
		elif i[1] == 'failed':
			data[1] += 1
		else:
			data[2] += 1
	return (data,data2)


def graph_2(task):
	"""
	return the js script for the graph 1 of the given task
	"""
	data = get_values(task)
	dataset1 = "{"+'label: "{1}",\n backgroundColor: ["rgba(0,200,0,0.8)","rgba(255,0,0,0.8)","rgba(130,130,130,0.5)","rgba(0,255,0,0.8)"],\n data: {0},\n'.format(data[0],task)+"}"
	dataset1 += ",{"+'label: "{1}",\n backgroundColor: ["rgba(0,200,0,0.8)", "rgba(255,0,0,0.8)","rgba(130,130,130,0.5)"],\n data: {0},\n'.format(data[1],task)+"}"
	#create and save the sript
	script = read_file("template2.html")
	script = script.replace("#data1#",dataset1)
	script = script.replace("#labels1#",str(["pass","fail","error","first_try"]))

	write_file("out.html",script)
	return script

graph_2("intersection")