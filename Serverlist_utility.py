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
    pretty_search_output = PrettyTable()
    pretty_search_output.add_row(lst[0])
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
    print(search_host_info("db01.example.com", service_list)

    # search_parser = argparse.ArgumentParser(description="Pretty prints information for exactly matched host.domain")
    # search_parser.add_argument("--search",

                               )
