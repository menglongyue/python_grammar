logging模块是Python内置的标准模块，主要用于输出运行日志，可以设置输出日志的等级、日志保存路径、日志文件回滚等。

**优点：**

- <font color = 'red'>定制化输出不同重要程度信息，过滤掉不重要信息</font>。有许多的重要性别级可供选择，`debug、info、warning、error 以及 critical`。通过赋予 `logger` 或者 `handler` 不同的重要级别，你就可以只输出错误消息到特定的记录文件中，或者在调试时只记录调试信息。
- <font color = 'red'>可自由选择将日志输出到哪里</font>，如控制台/日志文件/...，可通过不同的handler来配置。



## 1.logging整体框架

logging主要包括四大组成部分：

- **<font color = 'blue'>Loggers</font>**：提供程序直接调用的接口。

- **<font color = 'blue'>Handlers</font>**：决定日志输出位置。
- <font color = 'blue'>**Filters**</font>：对日志信息进行过滤， 提供更细粒度的日志输出。
- **<font color = 'blue'>Formatters</font>**：指定日志显示格式。

### 1.1 Loggers

`loggers`对象就是程序可以直接调用的一个日志接口，可以直接向生成的logger对象写入日志信息。`logger`并不是直接实例化使用的，而是通过`logging.getLogger(name)`来获取对象，事实上`logger`对象是单例模式，`logging`是多线程安全的，也就是无论程序中哪里需要打日志获取到的logger对象都是同一个。但是不幸的是logger并不支持多进程，这个在后面的章节再解释，并给出一些解决方案。

注意：loggers对象是有父子关系的，当没有父logger对象时它的父对象是root，当拥有父对象时父子关系会被修正。举个例子，logging.getLogger("abc.xyz") 会创建两个logger对象，一个是abc父对象，一个是xyz子对象，同时abc没有父对象，所以它的父对象是root。但是实际上abc是一个占位对象（虚的日志对象），可以没有handler来处理日志。但是root不是占位对象，如果某一个日志对象打日志时，它的父对象会同时收到日志，所以有些使用者发现创建了一个logger对象时会打两遍日志，就是因为他创建的logger打了一遍日志，同时root对象也打了一遍日志。



### 1.2 Handlers

Handlers 将logger发过来的信息进行准确地分配，送往正确的地方。如送往控制台/文件/控制台和文件/其他地方(进程管道之类的)。它决定了每个日志的行为，是之后需要配置的重点区域。

每个Handler同样有一个日志级别，一个logger可以拥有多个handler，也就是说logger可以根据不同的日志级别将日志传递给不同的handler。当然也可以相同的级别传递给多个handlers，这就根据需求来灵活的设置了。



### 1.3 Filters

Filters 提供了更细粒度的判断，来决定日志是否需要打印。原则上handler获得一个日志就必定会根据级别被统一处理，但是如果handler拥有一个Filter，就可以对日志进行额外的处理和判断。例如Filter能够对来自特定源的日志进行拦截，或者修改日志级别（修改后再进行级别判断）。logger和handler都可以安装filter甚至可以安装多个filter串联起来。





### 1.4 Formatters

Formatters 指定了最终某条记录打印的格式布局。Formatter会将传递来的信息拼接成一条具体的字符串，默认情况下Format只会将信息%(message)s直接打印出来。Format中有一些自带的LogRecord属性可以使用，如下表格:

![img](https://typora-images-1302473945.cos.ap-chengdu.myqcloud.com/images/202307201549939.png)

一个Handler只能拥有一个Formatter 因此如果要实现多种格式的输出只能用多个Handler来实现。



## 2.日志级别

在记录日志时, 日志消息都会关联一个级别。

级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG。

- **debug** : 打印所有级别的日志，详细的信息，通常只出现在诊断问题上。
- **info** : 打印info，warning，error，critical级别的日志，确认一切按预期运行。
- **warning** : 打印warning，error，critical级别的日志，如一些意想不到的事情发生，或表明一些问题可能在不久的将来发生(如磁盘空间低)。
- **error** : 打印error，critical级别的日志，更严重的问题，程序没能执行一些功能。
- **critical** : 打印critical级别，一个严重的错误，这表明程序本身可能无法继续运行。

总结：

![img](https://typora-images-1302473945.cos.ap-chengdu.myqcloud.com/images/202307201613800.png)

**如果需要显示低于某一级别的内容，可以引入`NOTSET`级别来显示。**







## 3.基本使用

### 3.1 简单使用

```python
import logging

# 这里仅仅用于控制台显示某些信息，不创建logger对象，直接使用logging下的各种级别打印方法

logging.info('This is a info message')
logging.debug('This is a debug message')
logging.warning('This is a warning message')

'''
WARNING:root:This is a warning message
'''
```

 默认情况下，logging将日志打印到屏幕，日志级别为WARNING；
		日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET，当然也可以自己定义日志级别。

缺点：

- 只能将日志打印到屏幕，无法输出到其他地方。



### 3.2 简单配置使用

```python
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.debug('this is debug message')  
logging.info('this is info message')  
logging.warning('this is warning message')  
```

这里简单使用basicConfig()函数来设置输出的格式。可以设置打印级别，格式以及输出到哪里。

缺点：整个程序只能创建一个basicConfig，也就是只能指定一个输出方式，要么打印到控制台，要么输出到文件/其他地方，无法同时打印并保存。同时，日志显示级别也只能指定一种。



### 3.3 定制化配置

如果你用 FileHandler 写日志，文件的大小会随着时间推移而不断增大。最终有一天它会占满你所有的磁盘空间。为了避免这种情况出现，你可以在你的生成环境中使用 RotatingFileHandler 替代 FileHandler。

```python
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

'''
file handler:
2023-07-20 16:43:31 - __main__ - WARNING - this is warning message
2023-07-20 16:43:31 - __main__ - ERROR - this is error message
2023-07-20 16:43:31 - __main__ - CRITICAL - this is critical message


stream handler:
2023-07-20 16:43:31 - __main__ - WARNING - this is warning message
2023-07-20 16:43:31 - __main__ - INFO - this is info message
2023-07-20 16:43:31 - __main__ - ERROR - this is error message
2023-07-20 16:43:31 - __main__ - CRITICAL - this is critical message
'''
```

设置2次setLevel原因(logger.setLevel与handler.setLevel)：**Logger中设置的级别决定它将传递给Handler的消息严重性。每个Handler设置的setLevel()决定了该处理程序将发送哪些消息**。也就是信息首先在logger那里过滤一下，然后传递到handler。



### 3.4 日志回滚

如果你用 FileHandler 写日志，并且模式为`a`，文件的大小会随着时间推移而不断增大。最终有一天它会占满你所有的磁盘空间。为了避免这种情况出现，你可以在你的生成环境中使用 RotatingFileHandler 替代 FileHandler。

```python
#!/usr/bin/env python
# coding=utf-8
'''
Author       : huangqj
Date         : 2023-07-20 16:57:10
LastEditors  : huangqj
LastEditTime : 2023-07-20 17:10:28
FilePath     : /python_grammar/1_Logger/demo04.py
Description  : Header Notes
 '''
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
from rich.progress import track

# 日志回滚

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 按照文件大小滚动
# 定义一个RotatingFileHandler，最多备份3个日志文件，每个日志文件最大1K
rHandler = RotatingFileHandler('demo04_size.log', maxBytes=1 * 1024, backupCount=3)
rHandler.setLevel(logging.INFO)

# 按照时间滚动
# when：是一个字符串，用于描述滚动周期的基本单位，字符串的值及意义如下：S M H D W等
# interval：滚动周期，单位有when指定，比如：when='D',interval=1，表示每天产生一个日志文件；
# backupCount：表示日志文件的保留个数；
tHandler = TimedRotatingFileHandler('demo04_time.log', when='S', interval=5, backupCount=3)
tHandler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
rHandler.setFormatter(formatter)
tHandler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logger.addHandler(rHandler)
logger.addHandler(tHandler)
logger.addHandler(stream_handler)


for i in track(range(100000)):
    logger.info("Start print log")
    logger.debug("Do something")
    logger.warning("Something maybe fail.")
    logger.info("Finish")

```



### 3.5 关于Filter

相比于日志级别，Filter 可定制性更丰富，可以在 Logger 和 Handler 上实现颗粒度更细的控制

```python
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
    
'''
2023-07-20 17:31:51 - __main__ - WARNING - Something maybe fail.
2023-07-20 17:31:51 - __main__ - WARNING - Something maybe fail.
2023-07-20 17:31:51 - __main__ - WARNING - Something maybe fail.
2023-07-20 17:31:51 - __main__ - WARNING - Something maybe fail.
2023-07-20 17:31:51 - __main__ - WARNING - Something maybe fail.
2023-07-20 17:31:51 - __main__ - WARNING - Something maybe fail.
2023-07-20 17:31:51 - __main__ - WARNING - Something maybe fail.
2023-07-20 17:31:51 - __main__ - WARNING - Something maybe fail.
2023-07-20 17:31:51 - __main__ - WARNING - Something maybe fail.
Working... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
'''

```



## 4.日志配置

程序配置日志有三种方式：

- 调用上述配置方法的Python代码显式创建Loggers、handlers和formatters
- 创建日志配置文件并使用fileConfig（）函数读取它
- 创建配置信息字典并将其传递给dictConfig（）函数



### 4.1 常规配置

前面内容都是使用第一种方式配置。



### 4.2 使用fileConfig配置

将配置相关东西单独写入一个文件，如：

```python
[loggers]
# 配置logger信息。必须包含一个名字叫做root的logger，当使用无参函数logging.getLogger()时，默认返回root这个logger，其他自定义logger可以通过 logging.getLogger("fileAndConsole") 方式进行调用
keys=root,file,fileAndConsole

[handlers]
# 定义声明handlers信息。
keys=fileHandler,consoleHandler

[formatters]
# 设置日志格式
keys=simpleFormatter

[logger_root]
# 对loggers中声明的logger进行逐个配置，且要一一对应,在所有的logger中，必须制定lebel和handlers这两个选项，对于非root handler，还需要添加一些额外的option，其中qualname表示它在logger层级中的名字，在应用代码中通过这个名字制定所使用的handler，即 logging.getLogger("fileAndConsole")，handlers可以指定多个，中间用逗号隔开，比如handlers=fileHandler,consoleHandler，同时制定使用控制台和文件输出日志
level=DEBUG
handlers=consoleHandler

[logger_file]
level=DEBUG
handlers=fileHandler
qualname=file
propagate=1

[logger_fileAndConsole]
level=DEBUG
handlers=fileHandler,consoleHandler
qualname=fileAndConsole
propagate=0

[handler_consoleHandler]
# 在handler中，必须指定class和args这两个option，常用的class包括 StreamHandler（仅将日志输出到控制台）、FileHandler（将日志信息输出保存到文件）、RotaRotatingFileHandler（将日志输出保存到文件中，并设置单个日志wenj文件的大小和日志文件个数），args表示传递给class所指定的handler类初始化方法参数，它必须是一个元组（tuple）的形式，即便只有一个参数值也需要是一个元组的形式；里面指定输出路径，比如输出的文件名称等。level与logger中的level一样，而formatter指定的是该处理器所使用的格式器，这里指定的格式器名称必须出现在formatters这个section中，且在配置文件中必须要有这个formatter的section定义；如果不指定formatter则该handler将会以消息本身作为日志消息进行记录，而不添加额外的时间、日志器名称等信息；
class=StreamHandler
args=(sys.stdout,)
level=DEBUG
formatter=simpleFormatter

[handler_fileHandler]
class=FileHandler
args=('dialog-analysis.log', 'a')
level=DEBUG
formatter=simpleFormatter

[formatter_simpleFormatter]
format=%(asctime)s - %(module)s - %(thread)d - %(levelname)s : %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

**配置文件的好处是：1.配置文件和代码的分离；2.非代码人员也能轻松定义配置文件的内容**

```python
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

'''
2023-07-20 17:38:51,609 - simpleExample - DEBUG - debug message
2023-07-20 17:38:51,609 - simpleExample - INFO - info message
2023-07-20 17:38:51,609 - simpleExample - WARNING - warn message
2023-07-20 17:38:51,609 - simpleExample - ERROR - error message
2023-07-20 17:38:51,609 - simpleExample - CRITICAL - critical message
'''
```

配置文件：

```

[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```





### 4.3 使用dictConfig配置

```python
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


'''
2023-07-20 17:49:31,250 demo07.py 74 INFO info message
2023-07-20 17:49:31,250 demo07.py 75 WARNING warning message
2023-07-20 17:49:31,250 demo07.py 76 ERROR error message
2023-07-20 17:49:31,250 demo07.py 77 CRITICAL critical message
2023-07-20 17:49:31,250 demo07.py 78 INFO ----------------------------------
2023-07-20 17:49:31,250 demo07.py 81 INFO info message
2023-07-20 17:49:31,250 demo07.py 82 WARNING warning message
2023-07-20 17:49:31,250 demo07.py 83 ERROR error message
2023-07-20 17:49:31,250 demo07.py 84 CRITICAL critical message
'''
```





参考：

- https://blog.csdn.net/hongxingabc/article/details/89295882
- https://blog.csdn.net/eettttttt/article/details/131630283



