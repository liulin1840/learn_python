# -*- coding: utf-8 -*-
#until.py 文本块生成器
import logging
import logging.config
logging.config.fileConfig('logging.conf')

# create logger
root_logger = logging.getLogger('root')
main_logger = logging.getLogger('main.util')

# 'application' code
main_logger.info("你好我们的文本标记项目开始了!")
def lines(file):
    for line in file:
        yield line #收集所遇到的行，
        main_logger.debug("line : %s" % line)
    yield '\n'                   #确保文件的最后一行是空行，否则就不知程序什么时候结束

def blocks(file):
    block = []

    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block != []:
            yield ''.join(block).strip()            #把列表连接成字符串
            main_logger.debug("block is %s " % block)
            block = []
