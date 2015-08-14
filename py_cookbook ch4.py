# python cookbook chapter 4
from random import random

def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)
        return self._children[-1]

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()
            
def make_rand_node(r):
	curr = Node(-1)
	li = [curr]
	for tag in r:
		if tag == 1:
			li.append(curr)
			curr = curr.add_child(Node(str(tag)))
		else:
			curr = li.pop()
	return curr

