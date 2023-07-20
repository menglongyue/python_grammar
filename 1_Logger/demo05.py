#!/usr/bin/env python
# coding=utf-8
'''
Author       : huangqj
Date         : 2023-07-20 16:57:10
LastEditors  : huangqj
LastEditTime : 2023-07-20 17:32:07
FilePath     : /python_grammar/1_Logger/demo05.py
Description  : Header Notes
 '''
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
from rich.progress import track

# 日志回滚

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 添加过滤器
# 如：只记录长度大于 10 的日志
class CustomFilter(logging.Filter):
    def filter(self, record):
        return len(record.msg) > 15
filter = CustomFilter()

# 按照文件大小滚动
# 定义一个RotatingFileHandler，最多备份3个日志文件，每个日志文件最大1K
rHandler = RotatingFileHandler('demo04_size.log', maxBytes=1 * 1024, backupCount=3)
rHandler.setLevel(logging.INFO)

# when：是一个字符串，用于描述滚动周期的基本单位，字符串的值及意义如下：
# interval：滚动周期，单位有when指定，比如：when='D',interval=1，表示每天产生一个日志文件；
# backupCount：表示日志文件的保留个数；
tHandler = TimedRotatingFileHandler('demo04_time.log', when='S', interval=5, backupCount=3)
tHandler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
rHandler.setFormatter(formatter)
tHandler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
stream_handler.addFilter(filter)

logger.addHandler(rHandler)
logger.addHandler(tHandler)
logger.addHandler(stream_handler)


for i in track(range(10)):
    logger.info("Start print log")
    logger.debug("Do something")
    logger.warning("Something maybe fail.")
    logger.info("Finish")


