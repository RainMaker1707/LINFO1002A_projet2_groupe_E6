import sqlite3
from fcts import read_file,write_file
from random import randint

def date_format(date):
	"""
	in: date string
	out: int number of minutes
	"""
	#2020-01-10T21:18:29.522+0100

	temp = date[0:10]
	days = 0

	if temp[0:4] == "2020":
		days += 365

		if temp[5:7] == "02":
			days += 31
		elif temp[5:7] == "03":
			days += 60
		elif temp[5:7] == "04":
			days += 91
		elif temp[5:7] == "05":
			days += 121
		elif temp[5:7] == "06":
			days += 152
		elif temp[5:7] == "07":
			days += 182
		elif temp[5:7] == "08":
			days += 213
		elif temp[5:7] == "09":
			days += 244
		elif temp[5:7] == "10":
			days += 274
		elif temp[5:7] == "11":
			days += 305
		elif temp[5:7] == "12":
			days += 335

	else:
		if temp[5:7] == "02":
			days += 31
		elif temp[5:7] == "03":
			days += 59
		elif temp[5:7] == "04":
			days += 90
		elif temp[5:7] == "05":
			days += 120
		elif temp[5:7] == "06":
			days += 151
		elif temp[5:7] == "07":
			days += 181
		elif temp[5:7] == "08":
			days += 212
		elif temp[5:7] == "09":
			days += 243
		elif temp[5:7] == "10":
			days += 273
		elif temp[5:7] == "11":
			days += 304
		elif temp[5:7] == "12":
			days += 334

	days += int(temp[8:10])

	return days


def get_entries(task):
	"""
	return list of entries
	[(/entry/),(course,task,date,username,result)]
	"""
	lst = []
	
	c = sqlite3.connect('inginious.sqlite').cursor()
		
	for row in c.execute("SELECT task, submitted_on from submissions"):
		if row[0] == task:
			lst.append(date_format(row[1]))
	c.close()

	return lst

def get_dates(task):
	"""
	return a tuple with the dates of beginig and end as ints
	"""
	dates = {}
	lst = []
	c = sqlite3.connect('inginious.sqlite').cursor()
	for row in c.execute("SELECT task, submitted_on from submissions group by submitted_on"):
		if row[0] == task:
			lst.append(date_format(row[1]))
			dates[row[1][5:10].replace("-","/")] = None

	c.close()
	lst.sort()

	temp = []
	for i in dates:
		temp.append(i)

	return (lst[0],lst[-1],temp)

def get_values(task):
	dates = get_dates(task)
	bars = dates[1]-dates[0]
	values = [0 for i in range(bars)]

	#get dates of each section
	interval = (dates[1]-dates[0])//bars

	#count the submissions
	temp = get_entries(task)
	for date in temp:
		values[date-dates[0]-1] += 1
			
	return (values,bars,dates[2])

def get_color():
	return(randint(50,200),randint(50,200),randint(50,200),0.7)

def graph_1(tasks):
	"""
	task can be a list of tuple of strings or a string
	return the js script for the graph 1 of the given task
	"""
	if tasks == str:
		tasks = [tasks]
	dataset = ""

	for task in tasks:
		temp = get_values(task)
		heights = temp[0]
		bars = temp[1]
		color = "Red"
		
		dataset += "{"+'label: "{2}",\n fill: true,\n borderColor: "rgba{1}",\n backgroundColor: "rgba{1}",\n data: {0},\n'.format(heights,str(get_color()),task)+"},"

	#create and save the sript
	script = read_file("template1.html")
	script = script.replace("#data#",dataset[:-1])
	script = script.replace("#labels#",str(temp[2]))

	print(temp[2])

	write_file("out.html",script)
	return script


graph_1(["intersection","Fibonacci"])