import sqlite3
from sqlite3 import Error

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

'''
def plot(sum_counts2, image_name):
    sum_counts1 = [0, 1, 2]
    sum_counts3 = ['Просрочено', 'В зоне риска', 'Сроки соблюдены']
    labels = ["Всего закупок: " + str(sum(sum_counts2))]
    parents = [""]
    values = [sum(sum_counts2)]

    # 2-й уровень, "лепестки" диаграммы
    second_level_dict = {x: sum_counts3[x] + ': ' + str(sum_counts2[x]) for x in sum_counts1}
    labels += map(lambda x: second_level_dict[x], sum_counts1)
    parents += [labels[0]] * len(sum_counts2)
    values += sum_counts2
    color_discrete_sequence = ['', '#ED1B1B', '#FF8000', '#32D624']

    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        marker=dict(colors=color_discrete_sequence)
    ))
    # fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

    fig.show()

    fig.write_image(image_name)

'''


def plot2(vals, image_name):
    # image_name_tmp = image_name
    labels = ["ok", "risk", "overdue"]
    fig, ax = plt.subplots()
    ax.pie(vals, labels=labels, wedgeprops=dict(width=0.5))
    fig.savefig(image_name)
    # image_name = image_name_tmp


def read_db(file_name):
    file = open(file_name, "r")
    db_list = []
    while True:
        line = file.readline()
        db_list.append(line.strip('    '))
    file.close()
    return db_list


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
