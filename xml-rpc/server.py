# -*- coding: UTF-8 -*-
from xmlrpclib import ServerProxy,Fault
from os.path import join,isfile,abspath
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys


#可避免试图停止并重启一个node，可能会得到端口已经在使用的错误
SimpleXMLRPCServer.allow_reuse_address=1

MAX_HISTORY_LENGTH = 6

UNHANDLED=100
ACCESS_DENIED = 200

class UnhandleQuery(Fault):
	"""无法处理的查询异常"""
	def __init__(self,message="could not handle the query"):
		Fault.__init__(self,UNHANDLED,message)

class AccessDenied(Fault):
	""" 无法访问"""
	def __init__(self,message='access denied'):
		Fault.__init__(self,ACCESS_DENIED,message)

def inside(dir,name):
	"""检查给定的目录里面是否有相应的文件"""
	dir = abspath(dir)
	name = abspath(name)
	return name.startswith(join(dir,""))

#取内部变量是个艺术活，
def getPort(url):
	"""从url中获取端口号"""
	name  = urlparse(url)[1]
	parts = name.split(':')
	return int(parts[-1])

class Node:
	def __init__(self,url,dirname,secret):
		self.url = url
		self.dirname = dirname
		self.secret = secret
		self.known = set()

	def query(self,query,history=[]):
		""" 查询要两个参数 名字 历史"""
		write_log('insert query function...')
		try:
			write_log('query result is %s '% self._handle(query))
			return self._handle(query)			
		except UnhandleQuery:
			history = history +[self.url]
			if len(history) >= MAX_HISTORY_LENGTH:raise
			return self._broadcast(query,history)

	def hello(self,other):
		"""将other添加到集合中去"""
		write_log('insert hello function...')
		self.known.add(other)
		return 0

	def fetch(self,query,secret):
		'获取文件，要先找到，并且密码正确,然后打开一个相同的文件，写入'
		write_log('insert fetch function ...')
		if self.secret != secret:raise AccessDenied
		result = self.query(query)
		f = open(join(self.dirname,query),'w+')
		write_log('create dirname %s' % join(self.dirname,query))
		f.write(result)
		f.close()
		return 0

	def _start(self):
		'启动服务'
		s= SimpleXMLRPCServer(("",getPort(self.url)),logRequests=False)
		s.register_instance(self)
		s.serve_forever()

	def _handle(self,query):
		'处理函数'
		write_log('insert _handle function ...')
		dir = self.dirname
		name = join(dir,query)
		if not isfile(name):raise UnhandleQuery
		if not inside(dir,name):raise AccessDenied
		write_log('name is %s ' % name)
		return open(name).read()

	def _broadcast(self,query,history):
		'广播出去'
		write_log('insert _broadcast function...')
		write_log('known is %s' % self.known.copy())
		for other in self.known.copy():
			if other in history:continue
			try:
				s = ServerProxy(other)
				return s.query(query,history)
			except Fault,f:
				if f.faultCode == UNHANDLED:pass
				else:self.known.remove(other)
			except :
				self.known.remove(other)
		raise UnhandleQuery

def write_log(line):
	log = open('server.log','a+')
	print >>log,line

def main():
	url,directory,secret = sys.argv[1:]
	n = Node(url,directory,secret)
	n._start()

if __name__ == '__main__':main()






