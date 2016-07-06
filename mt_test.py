# metaclass test
from time import ctime
from ipdb import set_trace


class mt(type):

    def __init__(self, name, bases, dct):
        # here the class A is created, self is <class A>
        print('mt.__init__', self.__name__, self)
        self.create_time2 = ctime()

    def __new__(cls, name, bases, dct):
        # here the class A is not created, at last in this function
        # 'return r' the r is <class A>
        print('mt.__new__')
        print('*'*10)
        print(cls, name, bases, dct)
        print('*'*10)
        r = super().__new__(cls, name, bases, dct)
        print('id', id(r))
        return r

    def __call__(self, *args, **kwargs):
        # when use a = A(x,y,z), this mean a = A.__call__(x,y,z),
        # in this function self is <class A> which created in __new__
        print('__call__')
        print(args)
        print(kwargs)
        # these args effect on obj.__init__
        instance = super().__call__(*args, **kwargs)
        instance.create_time = ctime()
        return instance


class mt2(type):

    def __new__(cls, name, bases, dct):
        cls.time = ctime()
        dct['time'] = cls.time
        print(cls)
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


class A(metaclass=mt):

    def __init__(self, a=1, b=2):
        self.a, self.b = a, b

    def func(self):
        print('in class @', self)


class B(metaclass=mt2):
    pass


class C(metaclass=Singleton):

    def __init__(self, x):
        self.x = x

    def func(self):
        print(self.x)

print()
print('*'*64)
print()


def from_metaclass(metaclass):
    def wrapper(cls):
        base = cls.__base__ if isinstance(cls.__base__, tuple) else (cls.__base__, )
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
