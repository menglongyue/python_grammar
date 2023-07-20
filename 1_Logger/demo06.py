#!/usr/bin/env python
# coding=utf-8
'''
Author       : huangqj
Date         : 2023-07-20 17:35:56
LastEditors  : huangqj
LastEditTime : 2023-07-20 17:37:46
FilePath     : /python_grammar/1_Logger/demo06.py
Description  : Header Notes
 '''
# 使用fileConfig（）函数读取配置文件
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleExample')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
