import sys
import re
import math


class Backpack:
    def __init__(self, backpack_size):
        self.__backpack_size = backpack_size
        self.__answer = list()
        self.__max_weight = 0
        self.__max_price = 0
        self.__gcd = 1

    def get_answer(self):
        return self.__answer

    def get_max_weight(self):
        return self.__max_weight

    def get_max_price(self):
        return self.__max_price

    def __find_gcd(self, weight):
        if len(weight) >= 2:
            self.__gcd = weight[0]
            for i in range(1, len(weight)):
                self.__gcd = math.gcd(self.__gcd, weight[i])

    def __scaling_weight(self, weight):
        for i in range(len(weight)):
            weight[i] = weight[i] // self.__gcd
        self.__backpack_size = self.__backpack_size // self.__gcd

    def __find_answer(self, matrix, columns, rows, weight):
        if matrix[rows][columns] == 0:
            return
        if matrix[rows][columns] != matrix[rows - 1][columns]:
            self.__find_answer(matrix, columns - weight[rows - 1], rows - 1, weight)
            self.__answer.append(rows)
            self.__max_weight = self.__max_weight + weight[rows - 1] * self.__gcd
        else:
            self.__find_answer(matrix, columns, rows - 1, weight)

    def matrix_creation(self, weight, price):
        self.__find_gcd(weight)
        self.__scaling_weight(weight)
        columns = self.__backpack_size + 1
        rows = len(weight) + 1
        matrix = [[0] * columns for i in range(rows)]
        for i in range(1, rows):
            for j in range(0, columns):
                if weight[i - 1] > j:
                    matrix[i][j] = matrix[i - 1][j]
                else:
                    matrix[i][j] = max(matrix[i - 1][j], matrix[i - 1][j - weight[i - 1]] + price[i - 1])
        self.__max_price = matrix[rows - 1][columns - 1]
        self.__find_answer(matrix, columns - 1, rows - 1, weight)


def main():
    input = sys.stdin
    output = sys.stdout
    weight = list()
    price = list()
    backpack = None
    flag = False
    for string in input:
        if re.match(r"\s*$", string):
            continue
        if not flag:
            if re.match(r"\d+$", string):
                flag = True
                backpack = Backpack(int(string))
            else:
                output.write("error\n")
        else:
            if re.match(r"\d+\s\d+$", string):
                split_string = string.split()
                weight.append(int(split_string[0]))
                price.append(int(split_string[1]))
            else:
                output.write("error\n")
    backpack.matrix_creation(weight, price)
    output.write(f"{backpack.get_max_weight()} {backpack.get_max_price()}\n")
    for object in backpack.get_answer():
        output.write(f"{object}\n")


if __name__ == '__main__':
    main()
