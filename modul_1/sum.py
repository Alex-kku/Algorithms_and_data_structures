import sys
import re

sum = 0
for string in sys.stdin:
    for match in re.findall(r'[-+]?\d+', string):
        sum += int(match)
print(sum)
