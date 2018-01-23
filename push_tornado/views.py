import json
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
from MalyshevAsk.models import User
REGISTRY = {}

class MainHandler(RequestHandler):
    def post(self):
        body = self.get_argument("msg")
        uid = self.get_argument("uid")
        conn = REGISTRY.get(uid)
        if conn:
            conn.write_message(json.dumps({"msg": body}))
            self.write("OK")
        else:
            self.write("NO")


class WSHandler(WebSocketHandler):
    def open(self, channel):
        print("WebSocket opened")
        print(channel)
        self.uid = channel
        REGISTRY[self.uid] = self

    def on_message(self, message):
        self.write_message(json.dumps({"msg": "hi, dog"}))

    def check_origin(self, origin):
        return True

    def on_close(self):
        print("WebSocket closed")
        del REGISTRY[self.uid]
