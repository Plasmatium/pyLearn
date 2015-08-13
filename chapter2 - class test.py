# sicp chapter2 ---- class test
# 15-8-14 0:08

def static_variables(f):
    svar_table = {}
    if 'inited' not in svar_table:
        svar_table = dict(f(None))
        svar_table['inited'] = None
    return svar_table

#@static_variables
class Account(object):
    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder
    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance
    def withdraw(self, amount):
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance = self.balance - amount
        return self.balance
    @static_variables
    def static(self):
        stab = {
            'interest': 0.02
            }
        return stab

def bind_method(value, instance):
    """Return a bound method if value is callable, or value otherwise."""
    if callable(value):
        def method(*args):
            return value(instance, *args)
        return method
    else:
        return value

def make_instance(cls):
    """Return a new object instance, which is a dispatch dictionary."""
    def get_value(name):
        return attributes[name]
    def set_value(name, value):
        attributes[name] = value
    attributes = cls.__dict__
    instance = {'get': get_value, 'set': set_value}
    return instance


