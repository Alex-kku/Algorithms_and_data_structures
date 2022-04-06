import sys
import re


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class MinHeap:
    def __init__(self):
        self.__keys_indexes_dictionary = dict()
        self.__heap = list()

    def __swap(self, child_index, parent_index):
        self.__heap[parent_index], self.__heap[child_index] = self.__heap[child_index], self.__heap[parent_index]
        self.__keys_indexes_dictionary[self.__heap[parent_index].key], self.__keys_indexes_dictionary[
            self.__heap[child_index].key] = parent_index, child_index

    def __bubble_down(self, index):
        child_index = 2 * index + 1
        while child_index < len(self.__heap):
            if child_index + 1 < len(self.__heap) and self.__heap[child_index + 1].key < self.__heap[child_index].key:
                child_index += 1
            if self.__heap[child_index].key < self.__heap[index].key:
                self.__swap(child_index, index)
                index = child_index
                child_index = 2 * index + 1
            else:
                break

    def __bubble_up(self, index):
        parent_index = (index - 1) // 2
        while parent_index >= 0:
            if self.__heap[parent_index].key > self.__heap[index].key:
                self.__swap(index, parent_index)
                index = parent_index
                parent_index = (index - 1) // 2
            else:
                break

    def add(self, key, value):
        if key in self.__keys_indexes_dictionary:
            raise Exception('error')
        self.__heap.append(Node(key, value))
        self.__keys_indexes_dictionary[key] = len(self.__heap) - 1
        self.__bubble_up(len(self.__heap) - 1)

    def set(self, key, value):
        if key not in self.__keys_indexes_dictionary:
            raise Exception('error')
        self.__heap[self.__keys_indexes_dictionary[key]].value = value

    def delete(self, key):
        if key not in self.__keys_indexes_dictionary:
            raise Exception('error')
        if self.__keys_indexes_dictionary[key] == len(self.__heap) - 1 or len(self.__heap) == 1:
            self.__heap.pop()
            del self.__keys_indexes_dictionary[key]
        else:
            index = self.__keys_indexes_dictionary[key]
            del self.__keys_indexes_dictionary[key]
            self.__heap[index] = self.__heap.pop()
            self.__keys_indexes_dictionary[self.__heap[index].key] = index
            if (index - 1) // 2 >= 0 and self.__heap[(index - 1) // 2].key > self.__heap[index].key:
                self.__bubble_up(index)
            else:
                self.__bubble_down(index)

    def search(self, key):
        if key not in self.__keys_indexes_dictionary:
            return None, None
        return self.__keys_indexes_dictionary[key], self.__heap[self.__keys_indexes_dictionary[key]].value

    def min(self):
        if not len(self.__heap):
            raise Exception('error')
        return self.__heap[0].key, self.__heap[0].value

    def max(self):
        if not len(self.__heap):
            raise Exception('error')
        start_index = len(self.__heap) // 2
        max_node = self.__heap[start_index]
        for index in range(start_index, len(self.__heap)):
            if self.__heap[index].key > max_node.key:
                max_node = self.__heap[index]
        return max_node.key, self.__keys_indexes_dictionary[max_node.key], max_node.value

    def extract(self):
        if not len(self.__heap):
            raise Exception('error')
        required_node = self.__heap[0]
        self.delete(required_node.key)
        return required_node.key, required_node.value

    def print(self, output):
        if not len(self.__heap):
            output.write("_\n")
            return
        output.write(f"[{self.__heap[0].key} {self.__heap[0].value}]\n")
        level = 2
        for index in range(1, len(self.__heap)):
            output.write(f"[{self.__heap[index].key} {self.__heap[index].value} {self.__heap[(index - 1) // 2].key}]")
            if index < (2 ** level) - 2:
                output.write(' ')
            elif index == (2 ** level) - 2:
                output.write('\n')
                level += 1
        if len(self.__heap) - 1 != (2 ** (level - 1) - 2):
            output.write('_' + ' _' * ((2 ** level) - len(self.__heap) - 2) + '\n')


def main():
    min_heap = MinHeap()
    input = sys.stdin  # input = open('input12.txt', 'r') - для варианта чтения из файла
    output = sys.stdout  # output = open('output.txt', 'w') - для варианта вывода в файл
    for string in input:
        if re.match(r"\s*$", string):
            continue
        try:
            if re.match(r"add\s-?\d+\s\S+$", string):
                split_string = string.split()
                min_heap.add(int(split_string[1]), split_string[2])
            elif re.match(r"set\s-?\d+\s\S+$", string):
                split_string = string.split()
                min_heap.set(int(split_string[1]), split_string[2])
            elif re.match(r"delete\s-?\d+$", string):
                min_heap.delete(int(string.split()[1]))
            elif re.match(r"search\s-?\d+$", string):
                index, value = min_heap.search(int(string.split()[1]))
                if index is None:
                    output.write("0\n")
                else:
                    output.write(f"1 {index} {value}\n")
            elif re.match(r"min$", string):
                min_key, mim_value = min_heap.min()
                output.write(f"{min_key} 0 {mim_value}\n")
            elif re.match(r"max$", string):
                max_key, max_index, max_value = min_heap.max()
                output.write(f"{max_key} {max_index} {max_value}\n")
            elif re.match(r"extract$", string):
                key, value = min_heap.extract()
                output.write(f"{key} {value}\n")
            elif re.match(r"print$", string):
                min_heap.print(output)
            else:
                output.write("error\n")
        except Exception as exc:
            output.write(str(exc) + '\n')
    # input.close() - для варианта чтения из файла
    # output.close() - для варианта вывода в файл


if __name__ == '__main__':
    main()
