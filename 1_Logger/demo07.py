#!/usr/bin/env python
# coding=utf-8
'''
Author       : huangqj
Date         : 2023-07-20 17:43:13
LastEditors  : huangqj
LastEditTime : 2023-07-20 17:49:29
FilePath     : /python_grammar/1_Logger/demo07.py
Description  : Header Notes
 '''
import logging.config

LOGGING_CONFIG = {
    # version - 表示版本，该键值为从1开始的整数。该key必选，除此之外，其它key都是可选。
    "version": 1,
    # formatters - 日志格式化器，其value值为一个字典，该字典的每个键值对都代表一个Formatter
    "formatters": {
        "default": {
            'format': '%(asctime)s %(filename)s %(lineno)s %(levelname)s %(message)s',
        },
        "plain": {
            "format": "%(message)s",
        },
    },
    # handlers - 日志处理器，其value值为一个字典，该字典的每个键值对都代表一个Handler
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
        },
        "console_plain": {
            "class": "logging.StreamHandler",
            "level": logging.INFO,
            "formatter": "plain"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": 20,
            "filename": "./log.txt",
            "formatter": "default",
        }
    },
    # loggers - 日志记录器，其value值为一个字典，该字典的每个键值对都代表一个Handler
    "loggers": {
        "console_logger": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "console_plain_logger": {
            "handlers": ["console_plain"],
            "level": "DEBUG",
            "propagate": False,
        },
        "file_logger": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        }
    },
    "disable_existing_loggers": True,
    "root": {
        "handlers": ["console"],
        # 取root level和console的level最严格的日志等级，下面输出为INFO等级
        "level": "DEBUG"
    },
}

# 运行测试
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("console_logger")
logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')
logger.info('----------------------------------')
logger = logging.getLogger("root")
logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')