# -*- coding: UTF-8 -*-
from xmlrpclib import ServerProxy,Fault
from cmd import Cmd
from random import choice
from string import lowercase
from server import Node,UNHANDLED
from threading import Thread
from time import sleep
import sys

HEAD_START = 0.1 #秒
SECRET_LENGTH = 100

def randomString(length):
	'返回给定长度的随机字符串'
	chars=[]
	letters = lowercase[:26]
	while length > 0:
		length -= 1
		chars.append(choice(letters))
	return ''.join(chars)

class Client(Cmd):	
	"""文本界面"""
	prompt='>'

	def __init__(self,url,dirname,urlfile):
		Cmd.__init__(self)
		self.secret = randomString(SECRET_LENGTH)
		n= Node(url,dirname,self.secret)
		t = Thread(target=n._start)
		t.setDaemon(1)
		t.start()
		sleep(HEAD_START)
		self.server  = ServerProxy(url)

		for line in open(urlfile):
			line = line.strip()
			write_log('line is %s' % line)
			self.server.hello(line)
				
	def do_fetch(self,arg):
		try:
			write_log('insert do_fetch function...')
			self.server.fetch(arg,self.secret)
		except Fault,f:
			if f.faultCode != UNHANDLED:raise
			print 'could not find the file',arg
	def do_exit(self,arg):
		print ''
		sys.exit()

	do_EOF = do_exit

def write_log(line):
	log = open('client.log','a+')
	print >>log,line

def main():

	urlfile,directory,url = sys.argv[1:]
	client = Client(url,directory,urlfile)
	client.cmdloop()

if __name__ == '__main__':
	main()