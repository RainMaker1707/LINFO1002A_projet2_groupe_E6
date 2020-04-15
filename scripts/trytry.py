from random import randint


def inter_fun_y_axe(top_list):
    top_list.reverse()
    x_axe = [0 for _ in range(len(top_list))]
    for i in range(len(top_list)):
        if i % 2 == 0:
            x_axe[int(i / 2)] = top_list[i]
        else:
            x_axe[- int(i/2 + 0.5)] = top_list[i]
    return x_axe


temp = ['a', 'b', 'c']
lst = list()
for i in range(len(temp)):
    lst.append((i, temp[i]))
lst.sort()
print(lst)
temp = inter_fun_y_axe(lst)
print(temp)

