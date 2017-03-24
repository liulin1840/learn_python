# -*- coding: utf-8 -*-
import  re
import logging
from  util import *
logger = logging.getLogger('main.handlers')
logger.info("处理程序开始")
class Handler:
    """
    处理程序 负责产生最终的标记文本，接受来自文本分析器的具体指令
    处理从Paraser调用的方法的对象 feed 方法可以将实际的文本交给处理程序去处理，
    prefix ；前缀的意思
    """
    #处理程序的超类
    def callback(self,prefix,name,*args):
        method = getattr(self,prefix+name,None)#self.start_list()
        logger.info('method = %s' % method)
        if callable(method):
            return method(*args)

    def start(self,name):
        self.callback('start_',name)
    def end(self,name):
        self.callback('end_',name)

    def sub(self,name):
        def substtution(match):
            resullt = self.callback('sub_',name,match)
            if resullt is None:
                resullt = match.group(0)
            return resullt
        return substtution

class HTMLRender(Handler):
    def start_document(self):
        print '<html><head><title>...</title></head></html>'
    def end_document(self):
        print'</body></html>'
    def start_paragraph(self):
        print'<p>'
    def end_paragraph(self):
        print '</p>'
    def start_heading(self):
        print '<h2>'
    def end_heading(self):
        print '</h2>'
    def start_list(self):
        print '<ul>'
    def end_list(self):
        print '</ul>'
    def start_listitem(self):
        print '<li>'
    def end_listitem(self):
        print '</li>'
    def start_title(self):
        print '<h1>'
    def end_title(self):
        print '</h1>'

    def sub_emphasis(self,match):
        return '<em>%s</em>' % match.group(1)
    def sub_url(self,match):
        return '<a href = "%s"> %s </a>' % (match.group(1),match.group(1))
    def sub_mail(self,match):
        return '<a href = "mailto:%s"> %s </a>' % (match.group(1),match.group(1))
    def feed(self,data):
        print data

#handler = HTMLRender()
#print re.sub(r'\*(.*?)\*',handler.sub('emphasis'),'this *is* a test ')
#this <em>is<em> a test