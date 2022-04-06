import sys
import re

set_size = -1
head = 0
tail = -1
queue = []
input = open(sys.argv[1], 'r')
output = open(sys.argv[2], 'w')
for string in input:
    if re.match(r"\s*$", string):
        continue
    if set_size < 0:
        if re.match(r"set_size\s[0-9]+$", string):
            set_size = int(string.split()[1])
            queue = [None] * set_size
        else:
            output.write("error\n")
    elif set_size >= 0:
        if re.match(r"push\s\S+$", string):
            if queue[(tail + 1) % set_size] != None:
                output.write("overflow\n")
            else:
                tail = (tail + 1) % set_size
                queue[tail] = string.split()[1]
        elif re.match(r"pop$", string):
            if head > tail and queue[head] == None:
                output.write("underflow\n")
            else:
                output.write(queue[head] + '\n')
                queue[head] = None
                head = (head + 1) % set_size
        elif re.match(r"print$", string):
            if head > tail and queue[head] == None:
                output.write("empty\n")
            elif head <= tail:
                output.write(' '.join(queue[head:tail + 1]) + '\n')
            elif head > tail:
                output.write(' '.join(queue[head:set_size]))
                output.write(' ' + ' '.join(queue[0:tail + 1]) + '\n')
        else:
            output.write("error\n")
input.close()
output.close()
