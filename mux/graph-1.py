from fcts import *

### does non work here, need makegraph()

def graph_submissions_repartitions(filename: str, task: str):
	"""
	task can be a list of tuple of strings or a string
	return the js script for the graph 1 of the given task
	"""
	data = get_data(filename,task)
	values = [0 for i in range(len(data[1]))]

	print(data)
	#count the submissions
	for date in data[2]:

		values[date-data[0]-1] += 1

	return make_graph("line","subs_rep",data[1],"evolition of submissions over the task duration",values)