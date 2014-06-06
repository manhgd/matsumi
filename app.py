#!/usr/bin/env python3
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.util
import time, os, os.path
import my.config
import my.cron

class App(tornado.web.Application):

    def __init__(self):
        # Routes
        handlers = []
        loaded = {}
        for url, assignee in my.config.routes:
            # Dynamic import handlers
            (module, handler) = assignee.split('@')
            if not module in loaded:
                loaded[module] = tornado.util.import_object('handler.' + module)
            handlers.append((url, getattr(loaded[module], handler)))
        handlers.append((r"/static/(.*)",  tornado.web.StaticFileHandler, {"path": os.path.join(my.config.path, 'static')}))
        super().__init__(handlers, **my.config.setting)
        self.config = my.config
        if not my.config.setting['debug']:
            import logging
            logging.basicConfig(level=logging.WARNING)

def main():
    tornado.options.parse_command_line()
    app = App()
    os.environ['TZ'] = my.config.timezone
    time.tzset()
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.listen(my.config.port, my.config.host)
    try:
        loop = tornado.ioloop.IOLoop.instance()
        cron = tornado.ioloop.PeriodicCallback(my.cron.daily, 24*3600*1000, loop)
        cron.start()
        loop.start()
    except KeyboardInterrupt:
        # Gracefully shutdown, add cleanup here if necessary
        print('Server got the signal. Bye!')
if __name__ == "__main__":
    main()
