from scripts.makeGraph import *
from mux.date_format import date_format, date_dic_to_list
import sqlite3

def graph_submissions_repartition(filename: str, task: str):
	"""
	:param filename:
	:param task:
	:retun:
	"""
	dates = {}
	days_lst = []
	dates_lst = []

	data = request(filename, "SELECT task, submitted_on from submissions WHERE task='{0}' ORDER BY submitted_on".format(task))
	if data == []:
		return "it apears, we have no submissions for this task."

	for entry in data:
		days_lst.append(date_format(entry[1]))
		dates[entry[1][0:10].replace("-", "/")] = None

	days_lst.sort()
	dates_lst = date_dic_to_list(dates,days_lst[-1]-days_lst[0],days_lst[0])

<<<<<<< Updated upstream
	values = [0 for _ in range(len(dates_lst))]
	for date in days_lst:
		values[date-days_lst[0]-1] += 1

	return make_graph("line", "subs_rep3", dates_lst, "Evolution of submissions over the task duration", values, True)
=======
	if data == [0, 0, 0]:
		return "it apears, we have no submissions for this task."
	else:
		return make_graph("line", "subs_rep3", data[1], "Evolution of submissions over the task duration", values, True)
>>>>>>> Stashed changes
