# coding: utf-8
import os
import sys
import logging

import tornado
import tornado.web
import tornado.httpserver
from tornado.options import define, options

from router.router import handlers
from util import grace, log
from config import conf

reload(sys)
sys.setdefaultencoding('utf-8')


class Application(tornado.web.Application):

    def __init__(self):
        settings = {
            "template_path": os.path.join(os.path.dirname(__file__), "template"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "debug": False,
            "gzip": True
        }
        tornado.web.Application.__init__(self, handlers, **settings)


def init():
    define("port", default=8080, help="run on the given port", type=int)
    options.parse_command_line()

    file_path = 'log/{}'.format(options.port)
    log.init_logging(file_path, conf.log_file_backups_num, conf.log_level)


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    grace.graceful_shutdown(http_server)
    logging.info("Server running on %s", options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    init()
    main()
