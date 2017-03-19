import functools
def log(text):
	def decorator(func):
		@functools.wraps(func)
		def wrapps(*args,**key):
			print '%s %s()' % (text,func.__name__)
			return func(*args,**key)
		return wrapps
	return decorator

@log('execute')
def now():
	print '2017-03-20'
if __name__ == '__main__':
	now()