import logging
import os
import re
import time
from pathlib import Path
from logging.handlers import RotatingFileHandler


class Log:
    # 日志打印等级
    LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    # 初始化一个logger进程
    logger = logging.getLogger()
    # 输出到控制台
    # cm = logging.StreamHandler()

    # 设置输出的最小等级
    logger.setLevel(LEVELS.get('default', logging.NOTSET))
    # cm.setLevel(logging.NOTSET)

    # 路径配置：获取当前脚本文件的父文件路径，并构造日志文件的存储路径：在当前.py文件的父文件路径的同级目录下创建文件夹logs
    pro_path = (str(Path(__file__).resolve().parent.parent))
    logs_path = os.sep.join([pro_path, 'logs'])
    if not Path(logs_path).exists():
        os.makedirs(logs_path)

    # chat-info.log 存放的是当前时间节点的日志，而chat-info,log,2023-xxxx.log 存放的是过去的日志
    # chat-error.log 存放错误日志文件的路径
    log_file = os.sep.join([logs_path, "chat-info.log"])
    err_file = os.sep.join([logs_path, "chat-err.log"])

    # 用于每天自动生成一个新的log文件
    log_handler = logging.handlers.TimedRotatingFileHandler(filename=log_file, when='D', interval=1,
                                                            backupCount=14)
    err_handler = logging.handlers.TimedRotatingFileHandler(filename=err_file, when='D', interval=1,
                                                            backupCount=14)

    # 定义日志文件的格式
    fmt_string = (
        '%(asctime)s [%(levelname)-8s| thread: %(thread)d | process: %(process)d] '
        '(path: %(pathname)s | line: %(lineno)-4d) '
        '[module: %(module)s | function: %(funcName)s] %(message)s')
    # 定义时间戳的格式
    datefmt = '%Y-%m-%d %H:%M:%S'
    # 创建一个 Formatter 实例
    formatter = logging.Formatter(fmt_string, datefmt=datefmt)

    # 加后缀。配置日志文件的后缀格式，以及匹配日志文件扩展名的正则表达式
    log_handler.suffix = "%Y-%m-%d.log"
    extMatch = r"^\d{4}-\d{2}-\d{2}(\.\w+)?$"
    log_handler.extMatch = re.compile(extMatch, re.ASCII)
    # 为错误日志文件设置同样的后缀和拓展名匹配
    err_handler.suffix = "%Y-%m-%d.log"
    extMatch = r"^\d{4}-\d{2}-\d{2}(\.\w+)?$"
    err_handler.extMatch = re.compile(extMatch, re.ASCII)

    # 添加设置。将 formatter 设置到 logger 上
    log_handler.setFormatter(formatter)
    err_handler.setFormatter(formatter)

    # 将输出格式添加至控制台
    # cm.setFormatter(color_fmt)
    # logger.addHandler(cm)

    # 给logger添加handler 添加内容到日志句柄中
    @classmethod
    def set_handler(cls, levels):
        # 根据传入的级别添加相应的日志句柄
        if levels == 'error':
            cls.logger.addHandler(cls.err_handler)
        cls.logger.addHandler(cls.log_handler)

    @classmethod
    def remove_handler(cls, levels):
        # 根据传入的级别移除相应的日志句柄
        if levels == 'error':
            cls.logger.removeHandler(cls.err_handler)
        cls.logger.removeHandler(cls.log_handler)

    # 定义不同级别的日志记录方法
    @classmethod
    def info(cls, message, *args, **kwargs):
        kwargs['stacklevel'] = 2
        cls.set_handler('info')
        cls.logger.info(message, *args, **kwargs)
        cls.remove_handler('info')

    @classmethod
    def debug(cls, message, *args, **kwargs):
        kwargs['stacklevel'] = 2
        cls.set_handler('debug')
        cls.logger.debug(message, *args, **kwargs)
        cls.remove_handler('debug')

    @classmethod
    def warning(cls, message, *args, **kwargs):
        kwargs['stacklevel'] = 2
        cls.set_handler('warning')
        cls.logger.warning(message, *args, **kwargs)
        cls.remove_handler('warning')

    @classmethod
    def error(cls, message, *args, **kwargs):
        kwargs['stacklevel'] = 2
        cls.set_handler('error')
        cls.logger.error(message, *args, **kwargs)
        cls.remove_handler('error')

    @classmethod
    def critical(cls, message, *args, **kwargs):
        kwargs['stacklevel'] = 2
        cls.set_handler('critical')
        cls.logger.critical(message, *args, **kwargs)
        cls.remove_handler('critical')

    @classmethod
    def set_level(cls, level_name):
        """
        用于更改日志级别的函数，在需要的地方，可以通过 Log.set_level("info") 修改为 info 等级
        """
        level = cls.LEVELS.get(level_name, logging.NOTSET)
        cls.logger.setLevel(level)


if __name__ == "__main__":
    Log.info('this is color1')
    Log.debug("This is debug message")
    Log.info("This is info message")
    Log.warning("This is warning message")
    Log.error("This is error")
    Log.critical("This is critical message")
