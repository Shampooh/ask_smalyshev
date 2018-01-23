from tornado import ioloop
from urls import make_app

PORT = 8888

if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    ioloop.IOLoop.current().start()