import sys
import re
from collections import deque


class Node:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left_child = None
        self.right_child = None

    def __str__(self):
        if self.parent is None:
            return f'[{self.key} {self.value}]'
        else:
            return f'[{self.key} {self.value} {self.parent.key}]'


class SplayTree:
    def __init__(self):
        self.__root = None

    def __right_rotation(self, node):
        grandparent = node.parent.parent
        node.parent.parent = node
        if grandparent:
            if grandparent.left_child == node.parent:
                grandparent.left_child = node
            else:
                grandparent.right_child = node
        else:
            self.__root = node
        if node.right_child:
            node.right_child.parent = node.parent
        node.parent.left_child = node.right_child
        node.right_child = node.parent
        node.parent = grandparent

    def __left_rotation(self, node):
        grandparent = node.parent.parent
        node.parent.parent = node
        if grandparent:
            if grandparent.right_child == node.parent:
                grandparent.right_child = node
            else:
                grandparent.left_child = node
        else:
            self.__root = node
        if node.left_child:
            node.left_child.parent = node.parent
        node.parent.right_child = node.left_child
        node.left_child = node.parent
        node.parent = grandparent

    def __splay(self, node):
        while node != self.__root:
            if node.parent == self.__root:
                if self.__root.left_child == node:
                    self.__right_rotation(node)
                else:
                    self.__left_rotation(node)
            else:
                if node.parent.left_child == node:
                    if node.parent.parent.left_child == node.parent:
                        self.__right_rotation(node.parent)
                        self.__right_rotation(node)
                    else:
                        self.__right_rotation(node)
                        self.__left_rotation(node)
                else:
                    if node.parent.parent.left_child == node.parent:
                        self.__left_rotation(node)
                        self.__right_rotation(node)
                    else:
                        self.__left_rotation(node.parent)
                        self.__left_rotation(node)

    def __find(self, key):
        required_node = self.__root
        if required_node is None:
            return None
        while required_node is not None:
            if key > required_node.key and required_node.right_child:
                required_node = required_node.right_child
            elif key < required_node.key and required_node.left_child:
                required_node = required_node.left_child
            else:
                return required_node

    def add(self, key, value):
        parent_added_node = self.__find(key)
        if parent_added_node is None:
            self.__root = Node(key, value)
        else:
            if key > parent_added_node.key:
                parent_added_node.right_child = Node(key, value, parent_added_node)
                self.__splay(parent_added_node.right_child)
            elif key < parent_added_node.key:
                parent_added_node.left_child = Node(key, value, parent_added_node)
                self.__splay(parent_added_node.left_child)
            else:
                self.__splay(parent_added_node)
                raise Exception('error')

    def set(self, key, value):
        updated_node = self.__find(key)
        self.__splay(updated_node)
        if (updated_node is None) or (key != updated_node.key):
            raise Exception('error')
        self.__root.value = value

    def search(self, key):
        required_node = self.__find(key)
        self.__splay(required_node)
        if (required_node is None) or (key != required_node.key):
            return None
        return self.__root.value

    def max(self):
        max_node = self.__root
        if max_node is None:
            raise Exception('error')
        while max_node.right_child is not None:
            max_node = max_node.right_child
        self.__splay(max_node)
        return max_node.key, max_node.value

    def min(self):
        min_node = self.__root
        if min_node is None:
            raise Exception('error')
        while min_node.left_child is not None:
            min_node = min_node.left_child
        self.__splay(min_node)
        return min_node.key, min_node.value

    def delete(self, key):
        deleted_node = self.__find(key)
        self.__splay(deleted_node)
        if (deleted_node is None) or (key != deleted_node.key):
            raise Exception('error')
        if deleted_node.right_child:
            if deleted_node.left_child:
                max_node = deleted_node.left_child
                while max_node.right_child is not None:
                    max_node = max_node.right_child
                self.__splay(max_node)
                self.__root.right_child = deleted_node.right_child
                if self.__root.right_child is not None:
                    self.__root.right_child.parent = self.__root
            else:
                self.__root = deleted_node.right_child
                self.__root.parent = None
        else:
            if deleted_node.left_child:
                self.__root = deleted_node.left_child
                self.__root.parent = None
            else:
                self.__root = None

    def print(self, output):
        if self.__root is None:
            output.write("_\n")
            return
        output_nodes = deque()
        output_nodes.append(self.__root)
        flag = False  # флаг для проверки конца вывода, если flag = True, значит в строке содержится вершина, у которой хотя бы один ребенок не '_'
        last_node = True  # флаг для проверки типа последнего элемента очереди, если flag = True, значит последний элемент очереди имеет тип Node
        node_number = 0
        tree_level = 0
        while True:
            current_node = output_nodes.popleft()
            if type(current_node) == Node:
                if type(current_node.left_child) == Node:
                    output_nodes.append(current_node.left_child)
                    flag = True
                    last_node = True
                else:
                    if last_node:
                        output_nodes.append(1)
                        last_node = False
                    elif node_number != 0:
                        output_nodes.append(output_nodes.pop() + 1)
                    else:
                        output_nodes.append(1)
                if type(current_node.right_child) == Node:
                    output_nodes.append(current_node.right_child)
                    flag = True
                    last_node = True
                else:
                    if last_node:
                        output_nodes.append(1)
                        last_node = False
                    else:
                        output_nodes.append(output_nodes.pop() + 1)
                node_number += 1
                output.write(str(current_node))
            else:
                if last_node:
                    output_nodes.append(current_node * 2)
                    last_node = False
                elif node_number != 0:
                    output_nodes.append(output_nodes.pop() + current_node * 2)
                else:
                    output_nodes.append(current_node * 2)
                node_number += current_node
                output.write('_' + ' _' * (current_node - 1))
            if node_number < 2 ** tree_level:
                output.write(' ')
            elif node_number == 2 ** tree_level and flag:
                output.write('\n')
                tree_level += 1
                node_number = 0
                flag = False
            else:
                output.write('\n')
                break


def main():
    splay_tree = SplayTree()
    input = sys.stdin  # input = open('path_to_input_file', 'r') - для варианта чтения из файла
    output = sys.stdout  # output = open('path_to_output_file', 'w') - для варианта вывода в файл
    for string in input:
        if re.match(r"\s*$", string):
            continue
        try:
            if re.match(r"add\s-?\d+\s\S+$", string):
                split_string = string.split()
                splay_tree.add(int(split_string[1]), split_string[2])
            elif re.match(r"set\s-?\d+\s\S+$", string):
                split_string = string.split()
                splay_tree.set(int(split_string[1]), split_string[2])
            elif re.match(r"delete\s-?\d+$", string):
                splay_tree.delete(int(string.split()[1]))
            elif re.match(r"search\s-?\d+$", string):
                value_required_node = splay_tree.search(int(string.split()[1]))
                if value_required_node is None:
                    output.write("0\n")
                else:
                    output.write(f"1 {value_required_node}\n")
            elif re.match(r"min$", string):
                min_key, mim_value = splay_tree.min()
                output.write(f"{min_key} {mim_value}\n")
            elif re.match(r"max$", string):
                max_key, max_value = splay_tree.max()
                output.write(f"{max_key} {max_value}\n")
            elif re.match(r"print$", string):
                splay_tree.print(output)
            else:
                output.write("error\n")
        except Exception as exc:
            output.write(str(exc) + '\n')
    # input.close() - для варианта чтения из файла
    # output.close() - для варианта вывода в файл


if __name__ == '__main__':
    main()
