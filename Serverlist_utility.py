from prettytable import PrettyTable
import csv
import argparse


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


def get_column_stats(column):
    col = set(column[1:])
    for i in col:
        cnt = column.count(i)
        print("{}: {}".format(i, cnt))


def search_column(searched_header, column_header):
    if searched_header.lower() == column_header.lower():
        return True


def stats(searched_column, columns):
    if search_column(searched_column, columns[0][0]):
        get_column_stats(columns[0])
    elif search_column(searched_column, columns[1][0]):
        get_column_stats(columns[1])
    elif searched_column.lower() == columns[2][0].lower():
        host_number = len((columns[2])-1)
        print("Number of hosts: {}".format(host_number))
    elif searched_column.lower() == columns[3][0].lower():
        backup = columns[3].count("True")
        print("Number of hosts with backup enabled: {}".format(backup))
    elif search_column(searched_column, columns[4][0]):
        get_column_stats(columns[4])
    elif search_column(searched_column, columns[5][0]):
        get_column_stats(columns[5])
    elif search_column(searched_column, columns[6][0]):
        get_column_stats(columns[6])


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
    args = parser.parse_args()

    if args.search:
        search_host_info(args.search, service_list, header)
    elif args.stat:
        stats(args.stat, columns)
    else:
        print(pretty_table_output)

