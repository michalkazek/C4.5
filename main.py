# -*- coding: utf-8 -*-
import math
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
    obj.split_row(file)
    obj.create_atr_dict()
    obj.count_attributes()
    obj.print_list(obj.column_instances_list)
    obj.print_dictionary(obj.decisions_for_attributes_dict)
    obj.entropy()

class Program:

    def __init__(self):
        self.input_matrix = []
        self.attr_column_number = 0
        self.row_number = 0
        self.column_instances_list = []
        self.decisions_for_attributes_dict = {}
        self.entropy_value = 0
    
    def split_row(self, file): 
        for row in file:
            splitted_row = (row.strip()).split(",")            
            splitted_row = list(map(int, splitted_row))
            self.attr_column_number = len(splitted_row)
            self.input_matrix.append(splitted_row)       
            self.row_number += 1 
        self.print_list(self.input_matrix)

    def print_list(self, input_list):  #development only method
        print()
        for line in input_list:
            print(line)

    def print_dictionary(self, input_dict):
        print()
        for x in input_dict:
            print("Column", x)
            for y in input_dict[x]:
                print("\tFor {0}".format(y),"->")
                for z in input_dict[x][y]:
                    print("\t\t decission {0} occurs: {1}".format(z, input_dict[x][y][z]))
            #print(input_dict[x][0])
        
    def create_atr_dict(self):
        for it in range(self.attr_column_number):
            self.column_instances_list.append({})
            if it != self.attr_column_number-1:
                self.decisions_for_attributes_dict[it] = {}
        
    def count_attributes(self):
        for row in self.input_matrix:
            for x in range(self.attr_column_number):
                if row[x] in self.column_instances_list[x]:
                    self.column_instances_list[x][row[x]] += 1
                else:
                    self.column_instances_list[x][row[x]] = 1
                if x != self.attr_column_number-1:
                    if row[x] not in self.decisions_for_attributes_dict[x]:
                        self.decisions_for_attributes_dict[x][row[x]] = {}
                    if row[self.attr_column_number-1] not in self.decisions_for_attributes_dict[x][row[x]]:
                        self.decisions_for_attributes_dict[x][row[x]][row[self.attr_column_number-1]] = 1
                    else:
                        self.decisions_for_attributes_dict[x][row[x]][row[self.attr_column_number-1]] += 1

    def entropy(self):
        tmp = self.column_instances_list[self.attr_column_number-1][0]/self.row_number
        tmp2 = self.column_instances_list[self.attr_column_number-1][1]/self.row_number
        self.entropy_value = tmp*math.log(tmp,2)+tmp2*math.log(tmp2,2)*-1
        print(self.entropy_value)
        





start()



