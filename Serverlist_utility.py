from prettytable import PrettyTable
import csv
import argparse


def get_host_domain(lst):
    lst.insert(2,("{}.{}".format(lst[2], lst[3])))
    lst.pop(3)
    lst.pop(3)
    return lst


def search_host_info(host, lst):
    searched_row= "None"
    for row, value in enumerate(lst):
        if host in value:
            searched_row = lst[row]
    pretty_search_output = PrettyTable(header)
    pretty_search_output.add_row(searched_row)
    return pretty_search_output


with open("sl.csv", newline="") as csvfile:
    sl = csv.reader(csvfile, delimiter=',')
    service_list = list(sl)

    for row, value in enumerate(service_list):
        service_list[row] = get_host_domain(service_list[row])
        for column in range(len(service_list[0])):
            if column in [1, 5, 6]:
                service_list[row][column] = service_list[row][column].capitalize()

    header = [h.capitalize() for h in service_list[0]]

    pretty_table_output = PrettyTable(header)
    for item in service_list[1:]:
        pretty_table_output.add_row(item)
    #need to set up an if condition to make sure that this is only displayed when there is no argument added
    print(pretty_table_output)

    search_parser = argparse.ArgumentParser()
    search_parser.add_argument("--search", help = "Pretty prints information for exactly matched host.domain")
    args = search_parser.parse_args()
    if args.search:
        print(search_host_info(args.search, service_list))
