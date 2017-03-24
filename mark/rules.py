# -*- coding: utf-8 -*-
class Rule:
    def action(self,block,handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    '''
    标题占一行，最多70个字符，并且不以冒号结尾 <h2></h2>
    '''
    type = 'heading'
    def condition(self,block):
        return not '\n' in block and len(block) <=70 and not block[-1] ==':'

class TitleRule(HeadingRule):
    '''
    题目是文档的 第一个块，但前提是他是大标题<h1> 只执行一次
    '''
    type = 'title'
    first = True
    def condition(self,block):
        if not self.first:
            return False
        self.first = False
        return HeadingRule.condition(self,block)

class ListItemRule(Rule):
    '''
    列表项 li
    '''
    type = 'listitem'
    def condition(self,block):
        return block[0] == '-'
    def action(self,block,handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True

class ListRule(ListItemRule):
    '''
    列表 ul 判断进来 与出去
    '''
    type = 'list'
    inside = False
    def condition(self,block):
        return  True
    def action(self,block,handler):
        if not self.inside and ListItemRule.condition(self,block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self,block):
            handler.end(self.type)
            self.inside = False

        return  False#结束

class ParagraphRule(Rule):
    type = 'paragraph'
    def condition(self,block):
        return  True