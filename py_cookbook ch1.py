###########################################
# Python cookbook learning
# chapter 1
# example in book testing & learning code
###########################################


from random import random
from collections import deque

def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for li in lines:
        if pattern in li:
            yield li, previous_lines
        previous_lines.append(li)

with open(r'C:\Users\Jonny.Wong\Documents\GitHub\pyLearn\function_decorator.py') as f:
 	for line, prevlines in search(f, 'python', 5):
 		for pline in prevlines:
 			print(pline, end='')
 		print(line, end='')
 		print('_' * 20)