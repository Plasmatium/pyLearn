# learn pipe, use pipe, control pipe, master pipe

from pipe import *
import re

#statistic with word frequncy in file s

def word_frequncy(filename):
	f = open(filename)
	content = f.read()
	f.close()

	return content|Pipe(lambda x: re.split('\W+', x))|Pipe(lambda x: (w for w in x if w != ''))|groupby(lambda x: x)|select(lambda x: (x[0], x[1]|count))|sort(key = lambda x: x[1], reverse=True)

