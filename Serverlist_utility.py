from prettytable import PrettyTable
import csv
import argparse
import json


def get_host_domain(lst):
    lst.insert(2,("{}.{}".format(lst[2], lst[3])))
    lst.pop(3)
    lst.pop(3)
    return lst


def search_host_info(host, serv_lst, header):
    searched_row = []
    for row, value in enumerate(serv_lst):
        if host in value:
            searched_row = serv_lst[row]
    result = zip(header, searched_row)
    for i in result:
        print("{:<11} | {:<}".format(i[0], i[1]))


def get_column_count(column):
    col = set(column[1:])
    for i in col:
        cnt = column.count(i)
        print("{}: {}".format(i, cnt))


def search_column(searched_header, column_header):
    if searched_header.lower() == column_header.lower():
        return True


def stats(searched_column, columns):
    if search_column(searched_column, columns[0][0]):
        get_column_count(columns[0])
    elif search_column(searched_column, columns[1][0]):
        get_column_count(columns[1])
    elif searched_column.lower() == columns[2][0].lower():
        host_number = len((columns[2])-1)
        print("Number of hosts: {}".format(host_number))
    elif searched_column.lower() == columns[3][0].lower():
        backup = columns[3].count("True")
        print("Number of hosts with backup enabled: {}".format(backup))
    elif search_column(searched_column, columns[4][0]):
        get_column_count(columns[4])
    elif search_column(searched_column, columns[5][0]):
        get_column_count(columns[5])
    elif search_column(searched_column, columns[6][0]):
        get_column_count(columns[6])


def get_row_index(column):
    row_index = []
    for i in column:
        loc_indexes = [m for m, x in enumerate(columns[6]) if x == i]
        row_index.append((i, loc_indexes))
    return row_index


def get_dictionary_host_loc(columns):
    loc_tup = list(zip(columns[6], columns[2]))
    loc_tup.pop(0)
    loc_values = dict(get_row_index(columns[6]))
    orphans = loc_values.get('')
    loc_values.pop('')
    loc_values.pop('Location')
    loc_values.update({"orphans": orphans})
    for x, y in loc_values.items():
        host_values = []
        for i in y:
            host_values.append(columns[2][i])
        loc_values[x] = {"hosts": host_values}
    print(json.dumps(loc_values, indent=4))


with open("sl.csv", newline="") as csvfile:
    sl = csv.reader(csvfile, delimiter=',')
    service_list = list(sl)

for row, value in enumerate(service_list):
    service_list[row] = get_host_domain(service_list[row])
    for column in range(len(service_list[0])):
        if column in [1, 5, 6]:
            service_list[row][column] = service_list[row][column].capitalize()

header = [h.capitalize() for h in service_list[0]]
columns = list(zip(*service_list))

pretty_table_output = PrettyTable(header)
for item in service_list[1:]:
    pretty_table_output.add_row(item)

parser = argparse.ArgumentParser()
parser.add_argument("--search", help="Pretty prints information for exactly matched host.domain")
parser.add_argument("--stat", help="Provides statistics for a specified column. Columns: os, env, host.domain,"
                                   "backup, update, location")
parser.add_argument("--list", nargs="?", const='c', help="Presents a list of servers grouped by their location. "
                                            "Hosts without group go to group orphans.")
parser.add_argument("--host", help="")
args = parser.parse_args()

if args.search:
    search_host_info(args.search, service_list, header)
elif args.stat:
    stats(args.stat, columns)
elif args.list:
    get_dictionary_host_loc(columns)
else:
    print(pretty_table_output)

