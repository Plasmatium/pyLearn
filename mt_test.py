# metaclass test

class mt(type):
	def __init__(self, *args, **kwargs):
		print(self, '__init__')
		print(args)
		print(kwargs)

	def __call__(self, *args, **kwargs):
		print(self, '__call__')
		print(args)
		print(kwargs)
