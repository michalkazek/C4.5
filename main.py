# -*- coding: utf-8 -*-
import math
import random


class FileReader:

    def __init__(self, input_percent):
        self.input_percent = input_percent
        self.file = ""
        self.number_of_columns = 0
        self.input_matrix = []
        self.test_matrix = []
        self.tree_matrix = []
        self.number_of_items = []
        self.repairing_values = []

    def get_data_from_file(self, path):
        self.file = open(path, "r")

    def split_row_from_input_file(self):
        for row in self.file:
            splitted_row = (row.strip()).split(",")
            self.number_of_columns = len(splitted_row)
            self.input_matrix.append(splitted_row)

    def create_structures(self):
        for it in range(self.number_of_columns):
            self.number_of_items.append({})

    def count_number_of_values(self):
        for row in self.input_matrix:
            for it in range(self.number_of_columns):
                if row[it] in self.number_of_items[it]:
                    self.number_of_items[it][row[it]] += 1
                else:
                    self.number_of_items[it][row[it]] = 1

    def find_best_values_to_repair_data(self):
        self.create_structures()
        self.count_number_of_values()
        for x in range(len(self.number_of_items)):
            best_value = 0
            quantity_of_best_value = 0
            for y in self.number_of_items[x]:
                if quantity_of_best_value < self.number_of_items[x][y]:
                    quantity_of_best_value = self.number_of_items[x][y]
                    best_value = y
            self.repairing_values.append(best_value)
        print(self.repairing_values)

    def repair_data(self):
        self.find_best_values_to_repair_data()
        for x in range(len(self.input_matrix)):
            for y in range(len(self.input_matrix[x])):
                if self.input_matrix[x][y] == "?":
                    self.input_matrix[x][y] = self.repairing_values[y]

    def divide_data(self):
        sequence_list = [x for x in range(len(self.input_matrix))]
        random.shuffle(sequence_list)
        for it in range(len(self.input_matrix)):
            if it < self.input_percent:
                self.test_matrix.append(self.input_matrix[sequence_list[it]])
            else:
                self.tree_matrix.append(self.input_matrix[sequence_list[it]])

    def get_test_matrix(self):
        return self.test_matrix


class Program:

    def __init__(self, input_matrix, number_of_columns):
        self.input_matrix = input_matrix
        self.number_of_columns = number_of_columns  # With decission column
        self.number_of_attributes = number_of_columns - 1  # Without decission column
        self.number_of_rows = len(input_matrix)
        self.column_values_list = []  # List of values in every column with their number
        self.decisions_for_attributes_dict = {}  # Dictionary contains the number of decisions instances for each attribute(column)
        self.info_values_list = []  # List containing info function values
        self.gain_values_list = []  # List containing gain for each attribute(column)
        self.gain_ratio_values_list = []  # List containing gain ratio for each attribute(column)
        self.divide_tree_dict = {}
        self.global_entropy_value = 0

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

    def calculate_global_entropy(self):
        for element in self.column_values_list[self.number_of_attributes]:
            p = self.column_values_list[self.number_of_attributes][element]/self.number_of_rows
            self.global_entropy_value += p * math.log2(p)
        self.global_entropy_value *= -1

    def calculate_local_entropy(self, column, attribute_value):
        entropy_value = 0
        for element in self.decisions_for_attributes_dict[column][attribute_value]:
            p = self.decisions_for_attributes_dict[column][attribute_value][element]/self.column_values_list[column][attribute_value]
            entropy_value += p * math.log2(p)
        entropy_value *= -1
        return entropy_value

    def calculate_info(self):
        for column in range(self.number_of_attributes):
            info_value = 0
            for attribute_value in self.column_values_list[column]:
                attribute_part = self.column_values_list[column][attribute_value] / self.number_of_rows
                info_value += attribute_part * self.calculate_local_entropy(column, attribute_value)
            self.info_values_list.append(info_value)

    def calculate_gain_for_attribute(self):
        for info_value in self.info_values_list:
            self.gain_values_list.append(self.global_entropy_value - info_value)

    def calculate_split_info(self, column):
        split_info = 0
        for element in self.column_values_list[column]:
            p = self.column_values_list[column][element]/self.number_of_rows
            split_info -= p * math.log2(p)
        return split_info

    def calculate_gain_ratio(self):
        for column in range(self.number_of_attributes):
            self.gain_ratio_values_list.append(self.gain_values_list[column]/self.calculate_split_info(column))

    def divide_tree(self):
        max_value = max(self.gain_values_list)
        max_index = self.gain_values_list.index(max_value)
        for x in self.column_values_list[max_index]:
            self.divide_tree_dict[x] = []
        for row in self.input_matrix:
            self.divide_tree_dict[row[max_index]].append(row)
        return self.divide_tree_dict, max_value, max_index


class Initial:

    def __init__(self):
        self.tree_depth_list = [0]
        self.attribute_value_list = [""]
        self.decisions = []
        self.divide = []

    def start(self):
        fr = FileReader(3)
        fr.get_data_from_file("test4.txt")
        fr.split_row_from_input_file()
        fr.repair_data()
        fr.divide_data()
        test_matrix = fr.get_test_matrix()
        node_list = [Program(fr.tree_matrix, fr.number_of_columns)]

        children_number_list = []
        tree_depth = -1
        it = 1

        for node in node_list:
            node.create_structures()
            node.count_number_of_values()
            node.calculate_global_entropy()
            node.calculate_info()
            node.calculate_gain_for_attribute()
            children_list, max_value, max_index = node.divide_tree()
            lock = True
            if max_value != 0:
                self.divide.append(max_index)
                children_number_list.append([0, len(children_list)])
                self.decisions.append('')
                tree_depth += 1
                for child in children_list:
                    self.attribute_value_list.insert(it, child)
                    node_list.insert(it, Program(children_list[child], node.number_of_columns))
                    self.tree_depth_list.insert(it, tree_depth + 1)
            else:
                #self.divide.append('')
                for x in children_list:
                    tmp = children_list[x][0][node.number_of_attributes]
                self.decisions.append(tmp)
                while lock:
                    children_number_list[tree_depth][0] += 1
                    if children_number_list[tree_depth][0] == children_number_list[tree_depth][1]:
                        children_number_list.pop(tree_depth)
                        tree_depth -= 1
                        if tree_depth < 0:
                            lock = False
                    else:
                        lock = False
            #self.print_tree(it, max_value, max_index)
            it += 1
        print("Values",self.attribute_value_list)
        print("Level",self.tree_depth_list)
        print("Dec",self.decisions)
        print("Divide", self.divide)
        return test_matrix

    def return_decision_tree(self):
        return self.attribute_value_list, self.tree_depth_list, self.decisions, self.divide,

    def print_tree(self, it, max_value, max_index):
        if it == 1:
            print("A{0}:".format(max_index))
        else:
            if max_value != 0:
                print("{0}{1}{2}A{3}:".format("------" * self.tree_depth_list[it - 1], self.attribute_value_list[it - 1], "--", max_index))
            else:
                print("{0}{1}".format("------" * self.tree_depth_list[it - 1], self.attribute_value_list[it - 1]))


class Testing:

    def __init__(self, input_attribute_value_list, input_tree_depth_list, input_decisions, input_divide, input_test_matrix):
        self.attribute_value_list = input_attribute_value_list
        self.tree_depth_list = input_tree_depth_list
        self.decisions = input_decisions
        self.divide = input_divide
        self.test_matrix = input_test_matrix
        self.unique_values = set(self.decisions)
        self.unique_values.remove("")
        self.unique_values = list(self.unique_values)
        self.error_matrix = [[0 for x in range(len(self.unique_values)+1)] for x in range(len(self.unique_values)+1)]

    def fill_error_matrix(self):
        self.error_matrix[0][0] = ''
        for x in range(1, len(self.unique_values)+1):
            self.error_matrix[x][0] = self.unique_values[x-1]
            self.error_matrix[0][x] = self.unique_values[x - 1]

    def test_rows(self):
        #input_row = ['1','0','1','1','0']
        current_deep_level = 1
        divide_index = 0  # index of self.divide value
        print("Unique", self.unique_values)

        for input_row in self.test_matrix:
            flag = True
            y = 1
            while flag:
                if input_row[self.divide[divide_index]] == self.attribute_value_list[y] and current_deep_level == self.tree_depth_list[y]:
                    if self.decisions[y] is not '':
                        for x in range(1, len(self.error_matrix)):
                            if self.decisions[y] == self.error_matrix[x][0]:
                                for z in range(1, len(self.error_matrix)):
                                    if input_row[-1] == self.error_matrix[0][z]:
                                        self.error_matrix[x][z] += 1
                                        flag = False
                                        break
                    else:
                        current_deep_level += 1
                        divide_index += 1
                y += 1

    def print_matrix(self):
        for x in self.error_matrix:
            print(x)

    #def calculate_recall(self):



init = Initial()
test = init.start()
a, b, c, d = init.return_decision_tree()

#test = Testing(a, b, c, d, test)
#test.fill_error_matrix()
#test.test_rows()
#test.print_matrix()