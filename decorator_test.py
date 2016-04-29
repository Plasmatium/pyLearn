#-------------------------------------------------------------------------
# File:         function_decorators.py
#
# Description:  Two examples of how to write your own decorators in Python.
#               Uses Python v3.0.
#
# (C) 2009 by Ariel Ortiz, Tecnologico de Monterrey, Campus Estado de Mexico.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#-------------------------------------------------------------------------

"""
#-------------------------------------------------------------------------
# 15-8-24 21:15 added by Jonny - Plasmatium
# dec is a decorator that makes clousure avoid "local variable 's' 
# referenced before assignment"
# see doc of dec()
#
#-------------------------------------------------------------------------
"""

from IPython.core.debugger import Tracer; set_trace = Tracer(colors='linux')

def memoize(f):
    cache = {}

    def helper(x):
        if x not in cache:
            cache[x] = f(x)
        return cache[x]
    return helper

def trace(f):
    def helper(x):
        call_str = '{0}({1})'.format(f.__name__, x)
        print('Calling {0} ...'.format(call_str))
        result = f(x)
        print('... returning from {0} = {1}'.format(call_str, result))
        return result
    return helper    

@trace
@memoize
def fib(n):
    if n in (0, 1):
        return n
    else:
        return fib(n - 1) + fib(n - 2)

def qfib(n):
    i = 0
    n0 = 0
    n1 = 1
    cur = 0
    while i < n:
        cur = n0 + n1   
        n0 = n1
        n1 = cur
        i += 1
    return cur

def qfib2(n):   #another qfib, use combined assignment
    i = 0
    a, b = 0, 1
    while i < n:
    	a, b = b, a+b
    	i += 1
    return b

def yfib():
    """
    yield virson of fib
    """
    a = b = 1
    yield a
    yield b
    while True:
        a, b = b, a+b
        yield b

def dec(f):
    """
    if use the def below, it won't work: "local variable 's' referenced before assignment"
    def dec(f):
         s = 0
         def w(x):
             s += f(x)
             return s
         return w
    """
    s = [0]
    def w(x):
        if x == 'reset':
            s[0] = 0
            return
        s[0] += f(x)
        return s[0]
    return w

class exp_on_next(object):
    def __init__(self, exp):
        self.exp = exp
    def __iter__(self):
        return self
    def __next__(self):
        try:
            n = self.gen.__next__()
            return n
        except self.exp as e:
            set_trace()
            return e
        except StopIteration as e:
            raise e
    def __call__(self, gen):
        self.gen = gen
        return self

def g(r):
    for x in range(r):
        if x==5:
            yield 1/0
        else:
            yield x

a = g(10)
b = exp_on_next(ZeroDivisionError)(a)
for x in b: print(x)

'''
http://stackoverflow.com/questions/11366064/handle-an-exception-thrown-in-a-generator
'''
