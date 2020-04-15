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


def leap(year):
    leap_flag = False
    if year % 4 == 0:
        leap_flag = True
    if year % 100 == 0:
        leap_flag = False
    if year % 400 == 0:
        leap_flag = True
    return leap_flag


