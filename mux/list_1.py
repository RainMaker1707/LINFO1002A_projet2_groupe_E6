import sqlite3

def request(filename: str, req: str):
    """
    :param filename: filename of the data base
    :param req: SQL request to send to bdd
    :return: a list of the tuple gave from SQL request
    """
    connection = sqlite3.connect(filename).cursor()
    lst = list()
    for row in connection.execute(req):
        lst.append(row)
    connection.close()
    return lst


def inter_fun_y_axe(top_list):
    top_list.reverse()
    x_axe = [0 for _ in range(len(top_list))]
    lenght = len(top_list)
    lst = []
    for i in range(len(top_list)):
        if i % 2 == 0:
        	x_axe[int(i / 2)] = top_list[i]
        else:
        	x_axe[- int(i/2 + 0.5)] = top_list[i]
        if i > 0 and top_list[i][0] == top_list[i-1][0]:
        	lenght -= 1
        else:
        	lst.append(top_list[i][0])
    lst.reverse()
    return x_axe, lenght, lst


def top_winrate(filename: str, mirored=False, *course: str, **task:str):
	"""
	"""
	pass

def top_subs_count(filename: str, top_size: int, mirored=False, by_course=False, by_task=False):
	"""
	:param filename:
	:param top_size:
	"""
	if by_course:
		req = "SELECT SUM(tried), course, username  FROM user_tasks GROUP BY username, course"
	elif by_task:
		req = "SELECT SUM(tried), task, username FROM user_tasks GROUP BY username, task"
	else:
		req = "SELECT SUM(tried), username FROM user_tasks GROUP BY username"

	data = request(filename,req)
	if mirored:
		data.sort(reverse=True)
	else:
		data.sort()

	lst, lenght, scores = inter_fun_y_axe(data[0:top_size])

	data = []
	titles = []

	for user in lst:
		for poss,score in enumerate(scores):
			print(poss,score)
			if score == user[0]:
				data.append(100/(poss+1))
				break
		if len(user) == 3:
			titles.append((user[0],user[1],user[2]))
		else:
			titles.append((user[0],user[1]))

	return data,titles

print(top_subs_count("inginious.sqlite",5))