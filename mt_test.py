# metaclass test
from time import ctime


class mt(type):

    def __init__(self, name, bases, dct):
        dct['ttt'] = ctime()
        super().__init__(name, bases, dct)

    def __call__(self, *args, **kwargs):
        print('__call__')
        print(args)
        print(kwargs)
        instance = super().__call__(*args, **kwargs)  # these args effect on obj.__init__
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
