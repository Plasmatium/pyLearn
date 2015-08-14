# python cookbook chapter 4
from random import random

def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

class Node(object):
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
            
def make_rand_node(root, level):
    if level == 0:
        return
    curr = root
    for i in range(int(random()*level)):
        curr.add_child(Node('level{0}.{1}'.format(level, i)))
    for cld in curr:
        make_rand_node(cld, level-1)

#use yield & generator to read file within specified block size
def read_file(fpath): 
   BLOCK_SIZE = 1024 
   with open(fpath, 'rb') as f: 
       while True: 
           block = f.read(BLOCK_SIZE) 
           if block: 
               yield block 
           else: 
               return

