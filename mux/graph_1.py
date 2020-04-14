from mux.fcts import *
from scripts.makeGraph import *


def graph_submissions_repartition(filename: str, task: str):
	"""
	task can be a list of tuple of strings or a string
	return the js script for the graph 1 of the given task
	"""
	data = get_data(filename, task)
	values = [0 for _ in range(len(data[1]))]
	for date in data[2]:
		values[date-data[0]-1] += 1

	if data == [0, 0, 0]:
        return "it apears, we have no submissions for this task."

	return make_graph("line", "subs_rep3", data[1], "Evolution of submissions over the task duration", values, True)
