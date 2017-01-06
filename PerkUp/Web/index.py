import tornado.web
import tornado.httpserver
import tornado.ioloop
from web_core import routes, options


class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, handlers=routes.getRoutes(), **options.app_options)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()