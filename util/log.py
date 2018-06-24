# coding: utf-8
import logging
from tornado.log import LogFormatter


def init_logging(file_path, backup_count, log_level):
    logger = logging.getLogger()
    logger.handlers = []
    channel = logging.handlers.TimedRotatingFileHandler(
        filename=file_path,
        when='midnight',
        backupCount=backup_count,
    )
    channel.setFormatter(LogFormatter(color=True))
    logger.setLevel(log_level.upper())
    logger.addHandler(channel)
