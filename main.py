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


class FileReader:

    @staticmethod
    def get_data_from_file(path):
        file = open(path, "r")
        return file


class Program:

    def __init__(self):
        self.input_matrix = []
        self.number_of_columns = 0  # With decission column
        self.number_of_attributes = 0  # Without decission column
        self.number_of_rows = 0
        self.column_values_list = []  # List of values in every column with their number
        self.decisions_for_attributes_dict = {}  # Dictionary contains the number of decisions instances for each attribute(column)
        self.global_entropy_value = 0
        self.local_entropy_value = 0
        self.info_value = 0

    @staticmethod
    def print_list(input_list, input_header=""):  # Development only method - used to print every list
        print("\n"+input_header)
        for line in input_list:
            print(line)

    @staticmethod
    def print_dictionary(input_dict, input_header=""):  # Development only method - used to print decisions dictionary
        print("\n"+input_header)
        for x in input_dict:
            print("Column", x)
            for y in input_dict[x]:
                print("\tFor {0}".format(y), "->")
                for z in input_dict[x][y]:
                    print("\t\t decission {0} occurs: {1}".format(z, input_dict[x][y][z]))

    def split_row_from_input_file(self, input_file):
        for row in input_file:
            splitted_row = (row.strip()).split(",")            
            splitted_row = list(map(int, splitted_row))
            self.number_of_columns = len(splitted_row)
            self.input_matrix.append(splitted_row)
        self.number_of_rows = len(self.input_matrix)
        self.number_of_attributes = self.number_of_columns-1

    def create_structures(self):
        for it in range(self.number_of_columns):
            self.column_values_list.append({})
            if it != self.number_of_attributes:
                self.decisions_for_attributes_dict[it] = {}
        
    def count_number_of_values(self):
        for row in self.input_matrix:
            for it in range(self.number_of_columns):
                if row[it] in self.column_values_list[it]:
                    self.column_values_list[it][row[it]] += 1
                else:
                    self.column_values_list[it][row[it]] = 1
                if it != self.number_of_attributes:
                    if row[it] not in self.decisions_for_attributes_dict[it]:
                        self.decisions_for_attributes_dict[it][row[it]] = {}
                    if row[self.number_of_attributes] not in self.decisions_for_attributes_dict[it][row[it]]:
                        self.decisions_for_attributes_dict[it][row[it]][row[self.number_of_attributes]] = 1
                    else:
                        self.decisions_for_attributes_dict[it][row[it]][row[self.number_of_attributes]] += 1

    def calculate_entropy(self):
        for dict_element in self.column_values_list[self.number_of_attributes]:
            p = self.column_values_list[self.number_of_attributes][dict_element]/self.number_of_rows
            self.global_entropy_value += (p * math.log2(p))
        self.global_entropy_value *= -1

    def calculate_local_entropy(self):
        for dict_element in self.decisions_for_attributes_dict[0][0]:
            p = self.decisions_for_attributes_dict[0][0][dict_element]/self.column_values_list[0][0]
            self.local_entropy_value += (p * math.log2(p))
        self.local_entropy_value *= -1

    def calculate_info(self):
        for x in self.column_values_list[0]:
            part = self.column_values_list[0][x] / self.number_of_rows
            self.calculate_local_entropy()
            self.info_value += part * self.local_entropy_value
            print(part)


class Initial:

    @staticmethod
    def start():
        file_reader = FileReader()
        file = file_reader.get_data_from_file("test2.txt")

        obj = Program()
        obj.split_row_from_input_file(file)
        obj.print_list(obj.input_matrix, "Input matrix:")
        obj.create_structures()
        obj.count_number_of_values()
        obj.print_list(obj.column_values_list, "Values in each column[column_values_list]:")
        obj.print_dictionary(obj.decisions_for_attributes_dict, "Decisions [decisions_for_attributes_dict]:")
        obj.calculate_entropy()
        obj.calculate_local_entropy()
        obj.calculate_info()
        print("\n"+"Global entropy: ", obj.global_entropy_value)
        print("\n"+"Local entropy: ", obj.local_entropy_value)


init = Initial()
init.start()
