# -*- coding: UTF-8 -*-
from xmlrpclib import ServerProxy,Fault
from client import randomString
from string import lowercase
from server import Node,UNHANDLED
from threading import Thread
from time import sleep
from os import listdir
import wx
import sys

HEAD_START = 0.1 #秒
SECRET_LENGTH = 100

class ListableNode(Node):
	def list(self):
		write_log('list function self.dirname = %s ' % self.dirname)
		return listdir(self.dirname)

class Client(wx.App):

	def __init__(self,url,dirname,urlfile):
		self.secret = randomString(SECRET_LENGTH)
		write_log('secret is %s ' % self.secret)
		n = ListableNode(url,dirname,self.secret)
		t = Thread(target=n._start)
		t.setDaemon(1)
		t.start()

		sleep(HEAD_START)
		self.server = ServerProxy(url)
		for line in open(urlfile):
			line = line.strip()
			self.server.hello(line)
		super(Client,self).__init__()
		write_log('end of __init__')

	def updataList(self):
		self.files.Set(self.server.list())
		write_log('self.server.list is %s ' % self.server.list())

	def OnInit(self):
		win = wx.Frame(None,title='File Sharing Client',size=(400,300))
		bkg = wx.Panel(win)
		self.input = input = wx.TextCtrl(bkg)
		submit = wx.Button(bkg,label='Fetch',size=(80,25))
		submit.Bind(wx.EVT_BUTTON,self.fetchHandler)
		hbox= wx.BoxSizer()

		hbox.Add(input,proportion=1,flag=wx.ALL|wx.EXPAND,border=10)
		hbox.Add(submit,flag=wx.TOP|wx.BOTTOM|wx.RIGHT,border=10)

		self.files = files = wx.ListBox(bkg)
		self.updataList()
		vbox= wx.BoxSizer(wx.VERTICAL)
		vbox.Add(hbox,proportion=0,flag=wx.EXPAND)
		vbox.Add(files,proportion=1,
		flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,border=10)

		bkg.SetSizer(vbox)
		win.Show()

		return True

	def fetchHandler(self,event):
		query = self.input.GetValue()
		try:
			self.server.fetch(query,self.secret)
			self.updataList()
		except Fault,f:
			if f.faultCode !=UNHANDLED:raise
			print 'could not find the file',query

def write_log(line):
	log = open('guiclient.log','a+')
	print >>log,line

def main():
	urlfile,directory,url = sys.argv[1:]
	client  = Client(url,directory,urlfile)
	client.MainLoop()

if __name__ == '__main__':
	main()
	