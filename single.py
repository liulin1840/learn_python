def singleton(cls,*args,**key):
	instancse = {}
	def _single():
		if cls not in instancse:
			instancse[cls] = cls(*args,**key)
		return instancse[cls]
	return _single

@singleton
class single(object):
	print 'ss'
if __name__ == '__main__':
	s1 = single()
	s2 = single()
	print id(s1)
	print id(s2)
