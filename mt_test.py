# metaclass test
from time import ctime
from ipdb import set_trace


class mt(type):

    def __init__(self, name, bases, dct):
        # here the class A is created, self is <class A>
        self.create_time2 = ctime()

    def __new__(cls, name, bases, dct):
        # here the class A is not created, at last in this function
        # 'return r' the r is <class A>
        r = super().__new__(cls, name, bases, dct)
        return r

    def __call__(self, *args, **kwargs):
        # when use a = A(x,y,z), this mean a = A.__call__(x,y,z),
        # in this function self is <class A> which created in __new__

        # these args effect on obj.__init__
        instance = super().__call__(*args, **kwargs)
        instance.create_time = ctime()
        return instance


class InheritException(Exception):

    '''Could not be inherited.'''


class mt2(type):

    def __new__(cls, name, bases, dct):
        cls.time = ctime()
        dct['time'] = cls.time

        return super().__new__(cls, name, bases, dct)


class Singleton(type):

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)
            return cls.instance
        else:
            return cls.instance


class NoInheritMeta(type):

    def __new__(cls, name, bases, dct):
        for base in bases:
            if isinstance(base, cls):
                raise InheritException('Could not be inherited from %s' % base)

        return super().__new__(cls, name, bases, dct)


class A(metaclass=mt):

    def __init__(self, a=1, b=2):
        self.a, self.b = a, b

    def func(self):
        pass


class B(metaclass=mt2):
    pass


class C(metaclass=Singleton):

    def __init__(self, x):
        self.x = x

    def func(self):
        pass


def from_metaclass(metaclass):
    def wrapper(cls):
        base = cls.__base__ if isinstance(
            cls.__base__, tuple) else (cls.__base__, )
        dct = cls.__dict__.copy()
        dct.pop('__weakref__', None)
        dct.pop('__dict__', None)
        return metaclass(cls.__name__, base, dct)
    return wrapper


@from_metaclass(mt)
class X():

    def __init__(self, a=10, b=100):
        self.a = a
        self.b = b


class NoIH(metaclass=NoInheritMeta):
    pass


'''
    protocol lib for python
    usage:
    >>>
    >>> @protocol
    ... class protocol_1():
    ...     def get_class_name(self):
    ...         return self.__class__.__name__
    ...
    >>> @extension(protocol_1)
    ... class MyClass():
    ...     pass
    ...
    >>> a = MyClass()
    >>> a.get_class_name()
    'MyClass'

    >>>
    >>> from hashlib import MD5
    >>> from time import ctime
    >>>
    >>> @protocol
    ... class protocol_2(ParentClass):
    ...     def func(self, *args, **kwargs):
    ...         pass
    ...

'''
