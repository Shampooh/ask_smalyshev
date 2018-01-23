from tornado.web import Application

from views import MainHandler, WSHandler


def make_app():
    return Application([
        (r"/publish/", MainHandler),
        (r"/listen/(.*)", WSHandler),
    ])
