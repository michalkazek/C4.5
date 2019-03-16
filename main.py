# -*- coding: utf-8 -*-

# 1.wczytywanie pliku
# 2.liczenie wystąpień elementu dla każdej kolumny
# 3.dla każdego z elementow policzyc ile decyzji jest 


def get_data_from_file(path):
    file = open(path, "r")
    return file

def start():
    file = get_data_from_file("test2.txt")

    obj = Program()
    obj.split_row(file)
    obj.create_atr_dict()
    obj.count_attributes()
    obj.print_dictionary(obj.decisions_for_attributes_dict)

class Program:

    def __init__(self):
        self.input_matrix = []
        self.attr_column_number = 0
        self.column_instances_list = []
        self.decisions_for_attributes_dict = {}
        self.tmp_list = []  # list created to test - contains all occured numbers
    
    def split_row(self, file): 
        for row in file:
            splitted_row = (row.strip()).split(",")            
            splitted_row = list(map(int, splitted_row))
            self.attr_column_number = len(splitted_row) - 1
            self.input_matrix.append(splitted_row)           
        self.print_list(self.input_matrix)

    def print_list(self, input_list):  #development only method
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
            self.decisions_for_attributes_dict[it] = {}
        
    def count_attributes(self):
        for row in self.input_matrix:
            for x in range(self.attr_column_number):
                if row[x] in self.column_instances_list[x]:
                    self.column_instances_list[x][row[x]] += 1
                else:
                    self.column_instances_list[x][row[x]] = 1
                if row[x] not in self.decisions_for_attributes_dict[x]:
                    self.decisions_for_attributes_dict[x][row[x]] = {}
                if row[self.attr_column_number] not in self.decisions_for_attributes_dict[x][row[x]]:
                    self.decisions_for_attributes_dict[x][row[x]][row[self.attr_column_number]] = 1
                else:
                    self.decisions_for_attributes_dict[x][row[x]][row[self.attr_column_number]] += 1

                # print(row[x])
        # print(self.column_instances_list)

    def x(self):
        print()
        for x in self.column_instances_list:
            print(x)
            for y in x:
                print(y, end=" ")
            print()
        print()





start()



