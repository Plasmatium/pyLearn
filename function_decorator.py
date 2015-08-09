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

from imp import reload

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

