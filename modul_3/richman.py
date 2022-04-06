import sys
import re


def main():
    riches = 0
    for string in sys.stdin:
        if re.match(r"\s*$", string):
            continue
        if re.match(r"\d+$", string):
            riches = int(string)
    winning_sequence = list()
    while riches != 0:
        if riches % 2 == 0:
            riches = riches // 2
            winning_sequence.append("dbl")
        elif riches == 3:
            riches -= 1
            winning_sequence.append("inc")
        elif riches == 1:
            winning_sequence.append("inc")
            break
        else:
            if (riches + 1) & (riches - 1) == (riches - 1):
                riches -= 1
                winning_sequence.append("inc")
            else:
                riches += 1
                winning_sequence.append("dec")
    for operation in winning_sequence[::-1]:
        print(operation)


if __name__ == '__main__':
    main()
