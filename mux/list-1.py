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

def top_winrate(filename: str, mirored=False, *course: str, **task:str):
	"""
	"""
	pass

def top_subs_count(filename: str, top_size, mirored=False, by_course = False, by_task = False):
	"""
	"""
	if by_course:
		req = "inginious.sqlite","SELECT SUM(tried), course, username  FROM user_tasks GROUP BY username, course"
	elif by_task:
		req = "SELECT SUM(tried), task, username FROM user_tasks GROUP BY username, task"
	else:
		req = "inginious.sqlite","SELECT SUM(tried), username FROM user_tasks GROUP BY username"

	data = request(filename,req)
	if mirored:
		data.sort(reverse=True)
	else:
		data.sort()

	return data[0,-top_size]