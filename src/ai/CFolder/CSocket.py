import socket

class CSocket:
    def __init__(self):
        self.server_conn = None #use when client mode
        self.clients = [] #use when server mode 

    def send_to_server(self, msg: str):
        if self.server_conn:
            try:
                self.server_conn.sendall(msg.encode())
            except Exception as e:
                print("Error sending to server:", e)

    def broadcast(self, msg: str, sender=None):
        for client in self.clients[:]:
            if client != sender:
                try:
                    client.sendall(msg.encode())
                except Exception as e:
                    print("Error sending to client:", e)
                    client.close()
                    self.clients.remove(client)    