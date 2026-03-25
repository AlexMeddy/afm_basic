import socket
import time
from CDebugLog import CDebugLog
from icecream import ic

class CSocket:
    def __init__(self):
        self.server_conn = None
        self.clients = []

        self.delayed_messages = []   # (send_time, client, message)

    def send_to_server(self, msg: str, delay=0):
        #ic(msg)
        if self.server_conn:
            send_time = time.time() + delay
            self.server_conn.sendall(msg.encode())
            CDebugLog.print_log(f"TO SERVER: {msg}", 1)

    def broadcast(self, msg: str, sender=None, delay=0):
        send_time = time.time() + delay

        for client in self.clients[:]:
            if client != sender:
                CDebugLog.print_log(f"TO CLIENT: {msg}", 1)
                client.sendall(msg.encode())

    def send_delayed_messages_old(self):
        return
        now = time.time()
        
        for item in self.delayed_messages[:]:
            send_time, client, msg = item

            if now >= send_time:
                try:
                    #print("TO SERVER: ", msg)
                    CDebugLog.print_log(f"msg sent: {msg}", 1)
                    client.sendall(msg.encode())
                except Exception as e:
                    try:
                        client.close()
                        if client in self.clients:
                            self.clients.remove(client)
                    except:
                        pass

                self.delayed_messages.remove(item)
