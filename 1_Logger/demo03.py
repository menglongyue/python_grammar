#!/usr/bin/env python
# coding=utf-8
'''
Author       : huangqj
Date         : 2023-07-20 16:34:12
LastEditors  : huangqj
LastEditTime : 2023-07-20 16:43:29
FilePath     : /python_grammar/1_Logger/demo03.py
Description  : Header Notes
 '''
import logging

# 创建logger对象
logger = logging.getLogger(__name__)

# 设置logger级别
logger.setLevel(logging.INFO)

# 创建handler对象
file_handler = logging.FileHandler('demo03.log', mode='w')
file_handler.setLevel(logging.WARNING)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# 创建formatter对象
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# 为handler对象设置formatter对象
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# 为logger对象添加handler对象
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


logger.debug('this is debug message')
logger.info('this is info message')
logger.warning('this is warning message')
logger.error('this is error message')
logger.critical('this is critical message')



