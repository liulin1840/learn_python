# -*- coding: utf-8 -*-
from asyncore import dispatcher
#这个dispatcher 类就是个套接字对象
from asynchat import async_chat
#async_chat类  收集客户端的数据并进行响应，
import socket,asyncore
#asyncore 框架，程序可以同时连接多个用户

PORT = 5005
NAME ='test_chat'
chat_log= open('chat_log','w+')

class EndSession(Exception):pass

class CommandHandle:
    '命令处理类'
    def unknow(self,session,cmd):
        '响应未知命令'
        session.push('unknow command :%s \r\n' % cmd)

    def handle(self,session,line):
        if not line.strip():return #如果行为空就空
        #以空格进行一次拆分
        parts = line.split(' ',1)
        cmd = parts[0]
        try:line =parts[1].strip()
        except IndexError :line = ''

        #试着调处理函数
        meth = getattr(self,'do_'+cmd,None)
        try:
            meth(session,line)
        except TypeError:
            self.unknow(session,cmd)

class Room(CommandHandle):
    def __init__(self,server):
        self.server = server
        self.sessions = []

    def add(self,session):
        self.sessions.append(session)

    def remove(self,session):
        self.sessions.remove(session)

    def broadcast(self,line):
        for session in self.sessions:
            session.push(line)

    def do_logout(self,session,line):
        raise EndSession

class LoginRoom(Room):
    def add(self,session):
        Room.add(self,session)
        #通过父类直接调用它的方法
        self.broadcast('welcome to %s \r\n' % self.server.name)

    def unknow(self,session,cmd):
        session.push('please log in Use "login <nick>"\r\n')

    def do_login(self,session,line):
        name = line.strip()
        if not name:
            session.push('please enter a name\r\n')
        elif name in self.server.users:
            session.push('the name "%s" is taken \r\n' %  name)
            session.push('please try again.\r\n')
        else:
            session.name = name
            session.enter(self.server.main_room)

class ChatRoom(Room):
    '为多用户聊天准备的房间'
    def add(self,session):
        #告诉所有的人有新用户进入
        self.broadcast(session.name+' has enter the room\r\n')
        self.server.users[session.name] = session
        Room.add(self,session)
    #离开
    def remove(self,session):
        Room.remove(self,session)
        self.broadcast(session.name+' has left the room\r\n')

    #发言
    def do_say(self,session,line):
        self.broadcast(session.name+':'+line+'\r\n')

    #查看登录用户
    def do_look(self,session,line):
        session.push('the following are in this room: \r\n')
        for other in self.sessions:
            session.push(other.name + '  \r\n')
    def do_who(self,session,line):
        session.push('the following are logged in ')
        for name in self.server.users:
            session.push(name + '\r\n')

class LogoutRoom(Room):
    def add(self,session):
        try :del self.server.users[session.name]
        except KeyError:pass

class ChatSession(async_chat):
    '处理服务器与用户之间连接的类'
    #构造函数做一些初始化工作
    def __init__(self,server,sock):
        async_chat.__init__(self,sock)
        self.server = server
        #server 应该是个对象，后面看
        self.set_terminator('\r\n')
        self.data=[]
        self.name=None
    #相当于设置一些属性值，好像调用了静态方法
    #问候语
        self.enter(LoginRoom(server))
        #self.push('welcome to %s \r\n' % self.server.name)

    #从当前房间移除自己，并将自身添加到下一个房间中
    def enter(self,room):
        try:cur = self.room
        except AttributeError:pass
        else:cur.remove(self)
        self.room  = room
        room.add(self)

    def collect_incoming_data(self, data):
        '覆盖，从套接字里面读取文本是调用'
        self.data.append(data)

        #data 在初始化函数里面定义了的，这里就可以用了

    def found_terminator(self):
        '覆盖，找到结束符，把列表里面的连接成字符串，然后广播出去'
        line  = ''.join(self.data)
        self.data = []
        try:self.room.handle(self,line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        '接受关闭函数'
        async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))
    #每个函数的调用都要包含对自身的引用self

class ChatServer(dispatcher):
    '接受连接并且产生单个会话类'
    def __init__(self,port,name):
        dispatcher.__init__(self)
        #调用父类的构造函数以后，就可以调用父类的相关方法了
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('',port))
        self.listen(5)
        self.name = name
        self.users = {}
        self.main_room = ChatRoom(self)

    def handle_accept(self):
        conn,addr = self.accept()
        #返回一个针对客户端的套接字和一个地址
        #self.sessions.append(ChatSession(self,conn))
        #第一个参数是服务器（传递的是对象，过去就可以调用方法），第二个参数套接字
        ChatSession(self,conn)
if __name__ =='__main__' :
    s = ChatServer(PORT,NAME)
    try:
        print 'chatserver on'
        asyncore.loop()
        
    except KeyboardInterrupt:print

   # create table
   # message(
   # id INT NOT NULL AUTO_INCREMENT,
   # subject VARCHAR(100) NOT NULL,
   #sender VARCHAR(20) NOT NULL,
    #reply_to INT,
    ##text MEDIUMTEXT NOT NULL,
    #PRIMARY KEY(id))