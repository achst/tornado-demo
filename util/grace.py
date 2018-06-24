# coding: utf-8
import time
import signal
import logging
from tornado.ioloop import IOLoop


def graceful_shutdown(http_server, max_time_out=3):
    loop = IOLoop.instance()

    def sig_handler(s, frame):
        logging.warning('Caught signal: %s, %s', s, frame)
        loop.add_callback_from_signal(shutdown)

    def shutdown():
        logging.info('Stopping http server')
        http_server.stop()

        logging.info('IOLoop will shutdown in %s seconds ...', max_time_out)
        deadline = time.time() + max_time_out

        def stop_loop():
            now = time.time()
            timeouts = [timeout for timeout in loop._timeouts if timeout.deadline < deadline]
            if now < deadline and (loop._callbacks or timeouts):
                return loop.add_timeout(now + 1, stop_loop)
            loop.stop()
            logging.info('Shutdown completed')

        stop_loop()

    for sig in (signal.SIGQUIT, signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, sig_handler)
