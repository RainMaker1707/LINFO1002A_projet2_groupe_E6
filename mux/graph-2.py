from mux.fcts import get_entries
from scripts.makeGraph import make_graph


def graph_2(filename: str, task: str):
	"""
	:param filename:
	:param task:
	:return:
	"""
	entries = get_entries(filename, task)
	users_results = {}
	data = [0, 0, 0, 0]

	for entry in entries:
		if entry[1] not in users_results:
			users_results[entry[1]] = entry[2]
			if entry[2] == 'success':
				data[3] += 1

		elif users_results[entry[1]] == 'failed':
			users_results[entry[1]] = entry[2]

	for result in users_results.items():
		if result[1] == 'success':
			data[0] += 1

		elif result[1] == 'failed':
			data[1] += 1

		else:
			data[2] += 1

	data[0] -= data[3]
	lst = ["success", "failed", "error"]
	return make_graph("line", "subs_rep", lst, "repartition of all submissions result", data)


def graph_3(filename: str, task: str):
	"""
	:param filename:
	:param task:
	:return:
	"""
	entries = get_entries(filename, task)
	data = [0, 0, 0]

	for entry in entries:
		if entry[2] == 'success':
			data[0] += 1
		elif entry[2] == 'failed':
			data[1] += 1
		else:
			data[2] += 1
	lst = ["success", "failed", "error"]
	return make_graph("line", "subs_rep", lst, "repartition of best performance by student", data)
