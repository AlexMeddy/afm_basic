import socket

class CSocket:
    def __init__(self):
        self.server_conn = None #use when client mode
        self.clients = [] #use when server mode 

        