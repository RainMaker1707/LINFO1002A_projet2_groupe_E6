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


def top_subs_count(filename: str, top_size: int, req: str, title: str, mirored=False):
	"""
	:param filename:
	:param top_size:
	:param req: the sql request of 2 or 3 elements
	:param title: the title of the graph on the page
	:param mirored: True = top worst, False = top best
	:return: 
	"""
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

	return make_graph("bar","top_subs_1",titles,title,data,True)

#1#"SELECT SUM(tried), username FROM user_tasks GROUP BY username"
#2#"SELECT SUM(tried), course, username  FROM user_tasks GROUP BY username, course"
#3#"SELECT SUM(tried), task, username FROM user_tasks GROUP BY username, task WHERE task='{0}'".format(#course#)