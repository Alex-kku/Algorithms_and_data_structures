import sys
import re
import math


class BitArray:
    def __init__(self, size):
        array_size = math.ceil(size / 32)
        self.__bit_array = [0] * array_size

    def get_bit_value(self, index):
        pointer = pow(2, index % 32)
        if self.__bit_array[index // 32] & pointer == 0:
            return False
        else:
            return True

    def set_bit_value(self, index):
        pointer = pow(2, index % 32)
        self.__bit_array[index // 32] = self.__bit_array[index // 32] | pointer


class BloomFilter:
    Mersenne_number_31 = 2 ** 31 - 1

    def __init__(self, n, p):
        k = -math.log2(p)
        if n == 0 or round(k) < 1:
            raise Exception('error')
        self.__hashes_num = round(k)
        self.__size = BloomFilter._search_size(n, k)
        self.__primes = self._search_primes(self.__hashes_num)
        self.__bit_array = BitArray(self.__size)

    @staticmethod
    def _search_size(n, k):
        return round(n * k / math.log(2))

    @staticmethod
    def _search_primes(number):
        primes_array = list()
        primes_array.append(2)
        cur_num = 3
        while len(primes_array) < number:
            limit = round(math.sqrt(cur_num)) + 1
            flag = True
            i = 0
            while flag and i < len(primes_array):
                if primes_array[i] <= limit:
                    if not cur_num % primes_array[i]:
                        flag = False
                else:
                    break
                i += 1
            if flag:
                primes_array.append(cur_num)
            cur_num += 2
        return primes_array

    def get_size(self):
        return self.__size

    def get_hashes_num(self):
        return self.__hashes_num

    def _search_hash(self, i, key):
        return int((((i + 1) * key + self.__primes[i]) % self.Mersenne_number_31) % self.__size)

    def add(self, key):
        for i in range(self.__hashes_num):
            index = self._search_hash(i, key)
            self.__bit_array.set_bit_value(index)

    def search(self, key):
        for i in range(self.__hashes_num):
            index = self._search_hash(i, key)
            if not self.__bit_array.get_bit_value(index):
                return False
        return True

    def print(self, output):
        for index in range(self.__size):
            if self.__bit_array.get_bit_value(index):
                output.write('1')
            else:
                output.write('0')


def main():
    input = sys.stdin  # input = open('path_to_input_file', 'r') - для варианта чтения из файла
    output = sys.stdout  # output = open('path_to_output_file', 'w') - для варианта вывода в файл
    bloom_filter = None
    for string in input:
        if re.match(r"\s*$", string):
            continue
        if bloom_filter is None:
            try:
                if re.match(r"set\s\d+\s0.\d+$", string):
                    split_string = string.split()
                    bloom_filter = BloomFilter(int(split_string[1]), float(split_string[2]))
                    n = bloom_filter.get_size()
                    k = bloom_filter.get_hashes_num()
                    output.write(f"{n} {k}\n")
                else:
                    output.write("error\n")
            except Exception as exc:
                output.write(str(exc) + '\n')
        else:
            if re.match(r"add\s\d+$", string):
                bloom_filter.add(int(string.split()[1]))
            elif re.match(r"print$", string):
                bloom_filter.print(output)
                output.write("\n")
            elif re.match(r"search\s\d+$", string):
                if bloom_filter.search(int(string.split()[1])):
                    output.write("1\n")
                else:
                    output.write("0\n")
            else:
                output.write("error\n")
    # input.close() - для варианта чтения из файла
    # output.close() - для варианта вывода в файл


if __name__ == '__main__':
    main()
