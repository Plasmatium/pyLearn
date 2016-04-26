# descriptor test

from weakref import WeakKeyDictionary
from IPython.core.debugger import Tracer; set_trace = Tracer(colors='linux')

#normal descriptor
class Desc(object):
	def __init__(self, default=None, callbacks=[], asserts=[]):
		self.default = default
		self.callbacks = callbacks
		self.asserts = asserts
		self.data = WeakKeyDictionary()

	def __get__(self, instance, owner):
		if instance:
			return self.data.get(instance, self.default)
		else:
			return self

	def __set__(self, instance, value):
		this_desc = self
		for func in self.asserts:
			try:
				assert(func(this_desc, instance, value))
			except:
				err_str = '\n\tfunc is %s\n\tdescriptor is %s\n\tinstance is %s\n\tvalue is %s'%(func, this_desc, instance, value)
				raise AssertionError(err_str)

		for func in self.callbacks:
			this_desc = self
			func(this_desc, instance, value)

		self.data[instance] = value

	def add_callback(self, func):
		self.callbacks.append(func)

	def add_assert(self, func):
		#assert func is function
		self.asserts.append(func)


#test class
class Test(object):
	x = Desc(0)
	y = Desc(1)
	z = Desc()
	def __init__(self, x=0, y=10, z=100):
		self.x = x
		self.y = y
		self.z = z
	def __repr__(self):
		return str((self.x, self.y, self.z))

if __name__ == '__main__':
	#assert func examples:
	def is_gt5(desc, instance, value):
		if value <= 5:
			raise ValueError('value: %s <= 5'%value)
		else:
			return True