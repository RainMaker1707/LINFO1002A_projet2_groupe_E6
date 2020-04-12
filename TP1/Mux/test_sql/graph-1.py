import sqlite3
from fcts import read_file,write_file

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

	return lst

def get_dates(task):
	"""
	return a tuple with the dates of beginig and end as ints
	"""

	lst = []
	c = sqlite3.connect('inginious.sqlite').cursor()
	for row in c.execute("SELECT task, submitted_on from submissions group by submitted_on"):
		if row[0] == task:
			lst.append(date_format(row[1]))

	lst.sort()

	return (lst[0],lst[-1])

def get_values(task):
	dates = get_dates(task)
	bars = dates[1]-dates[0]
	values = [0 for i in range(bars)]

	#get dates of each section
	interval = (dates[1]-dates[0])//bars

	print(dates,bars)
	#count the submissions
	for date in get_entries(task):
		values[date-dates[0]-1] += 1

	print(values)
			
	return (values,bars)

def get_color():
	return(200,0,0,0.7)

def graph_1(task):
	"""
	return the js script for the graph 1 of the given task
	"""
	temp = get_values(task)
	heights = temp[0]
	bars = temp[1]
	color = "Red"
	dataset = ""
	dataset += "{"+'label: "{2}",\n fill: true,\n borderColor: "rgba{1}",\n backgroundColor: "rgba{1}",\n data: {0},\n spanGaps: true,\n'.format(heights,str(get_color()),task)+"}"

	labels = '[""'
	for i in range(bars):
		labels += ',""'
	labels += ']'

	#create and save the sript
	script = read_file("template.html")
	script = script.replace("#data#",dataset)
	script = script.replace("#labels#",labels)

	write_file("out.html",script)
	return script


graph_1("intersection")