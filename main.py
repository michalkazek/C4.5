# -*- coding: utf-8 -*-
import math
# to do list
# 1.wczytywanie pliku
# 2.liczenie wystąpień elementu dla każdej kolumny
# 3.dla każdego z elementow policzyc ile decyzji jest 
# 4.etropia (napisać funkcje)
# 5.info
# 6.prztosr_infomracji (gain)
# 7.split_info


def get_data_from_file(path):
    file = open(path, "r")
    return file

def start():
    file = get_data_from_file("test2.txt")

    obj = Program()
    obj.split_row_from_input_file(file)
    obj.print_list(obj.input_matrix, "Input matrix:")
    obj.create_structures()
    obj.count_attributes()
    obj.print_list(obj.column_values_list, "Values in each column:")
    obj.print_dictionary(obj.decisions_for_attributes_dict, "Decisions:")
    obj.count_entropy()
    print("Entropy: ", obj.entropy_value)


class Program:

    def __init__(self):
        self.input_matrix = []
        self.column_number = 0
        self.row_number = 0
        self.column_values_list = []  # List of values in every column with their number
        self.decisions_for_attributes_dict = {}  # Dictionary contains the number of decisions instances for each attribute(column)
        self.entropy_value = 0

    @staticmethod
    def print_list(input_list, input_header=""):  # Development only method - used to print every list
        print("\n"+input_header)
        for line in input_list:
            print(line)

    @staticmethod
    def print_dictionary(input_dict, input_header=""): # Development only method - used to print decisions dictionary
        print("\n"+input_header)
        for x in input_dict:
            print("Column", x)
            for y in input_dict[x]:
                print("\tFor {0}".format(y),"->")
                for z in input_dict[x][y]:
                    print("\t\t decission {0} occurs: {1}".format(z, input_dict[x][y][z]))

    def split_row_from_input_file(self, input_file):
        for row in input_file:
            splitted_row = (row.strip()).split(",")            
            splitted_row = list(map(int, splitted_row))
            self.column_number = len(splitted_row)
            self.input_matrix.append(splitted_row)
        self.row_number = len(self.input_matrix)

    def create_structures(self):
        for it in range(self.column_number):
            self.column_values_list.append({})
            if it != self.column_number-1:
                self.decisions_for_attributes_dict[it] = {}
        
    def count_attributes(self):
        for row in self.input_matrix:
            for x in range(self.column_number):
                if row[x] in self.column_values_list[x]:
                    self.column_values_list[x][row[x]] += 1
                else:
                    self.column_values_list[x][row[x]] = 1
                if x != self.column_number-1:
                    if row[x] not in self.decisions_for_attributes_dict[x]:
                        self.decisions_for_attributes_dict[x][row[x]] = {}
                    if row[self.column_number-1] not in self.decisions_for_attributes_dict[x][row[x]]:
                        self.decisions_for_attributes_dict[x][row[x]][row[self.column_number-1]] = 1
                    else:
                        self.decisions_for_attributes_dict[x][row[x]][row[self.column_number-1]] += 1

    def count_entropy(self):
        for dict_element in self.column_values_list[self.column_number-1]:
            p = self.column_values_list[self.column_number-1][dict_element]/self.row_number
            self.entropy_value += (p * math.log2(p))
        self.entropy_value *= -1


start()



