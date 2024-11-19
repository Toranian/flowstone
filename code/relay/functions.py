from ewma import EWMA
from sock import WebSocketServer

class App:

    def __init__(self):
        # self.focus = FocusSession()
        # self.relay = RelaySession()
        self.ewma = EWMA()
        self.socket = WebSocketServer()
