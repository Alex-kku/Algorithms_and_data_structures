import sys
import re

set_size = -1
head = -1
stack = []
for string in sys.stdin:
    if re.match(r"\s*$", string):
        continue
    if set_size < 0:
        if re.match(r"set_size\s[0-9]+$", string):
            set_size = int(string.split()[1])
            stack = [None] * set_size
        else:
            print("error")
    elif set_size >= 0:
        if re.match(r"push\s\S+$", string):
            if head + 1 > set_size - 1:
                print("overflow")
            else:
                head += 1
                stack[head] = string.split()[1]
        elif re.match(r"pop$", string):
            if head == -1:
                print("underflow")
            else:
                print(stack[head])
                stack[head] = None
                head -= 1
        elif re.match(r"print$", string):
            if head == -1:
                print("empty")
            else:
                print(' '.join(stack[:head + 1]))
        else:
            print("error")
