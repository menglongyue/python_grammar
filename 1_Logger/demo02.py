#!/usr/bin/env python
# coding=utf-8
'''
Author       : huangqj
Date         : 2023-07-20 16:20:55
LastEditors  : huangqj
LastEditTime : 2023-07-20 16:27:55
FilePath     : /python_grammar/1_Logger/demo02.py
Description  : Header Notes
 '''
import logging

# 这里简单使用basicConfig()函数来设置输出的格式
'''
# basicConfig()函数中可设置的参数有：
  - level: 设置日志级别，默认为logging.WARNING
  - format: 设置日志格式，默认为%(levelname)s:%(name)s:%(message)s
        %(levelno)s: 打印日志级别的数值
        %(levelname)s: 打印日志级别名称
        %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
        %(filename)s: 打印当前执行程序名
        %(funcName)s: 打印日志的当前函数
        %(lineno)d: 打印日志的当前行号
        %(asctime)s: 打印日志的时间
        %(thread)d: 打印线程ID
        %(threadName)s: 打印线程名称
        %(process)d: 打印进程ID
        %(message)s: 打印日志信息
  - datefmt: 设置日期格式
  - filename: 设置日志输出的文件
  - filemode: 设置日志输出文件的打开模式
  - stream: 设置输出流，可以指定输出到sys.stderr, sys.stdout或者文件，默认输出到sys.stderr，当stream和filename同时指定时，stream被忽略
  - handlers: 如果没有指定handlers，将会创建一个默认的handler，如果指定了handlers则不会创建默认handler
'''


# 1.不实用handlers参数
# 不指定filename就是输出到控制台， 指定filename就会输出到文件
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.debug('this is debug message')  
logging.info('this is info message')  
logging.warning('this is warning message')  