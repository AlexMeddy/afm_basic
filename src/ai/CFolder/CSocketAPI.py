import socket
import time
from CDebugLog import CDebugLog
from icecream import ic
import requests

class CSocket:
    def __init__(self):
        self.server_url = None  # e.g. http://127.0.0.1:5000

    def send_to_server(self, endpoint: str, data: dict = None):
        try:
            url = f"{self.server_url}/{endpoint}"

            print(f"\n[CLIENT -> SERVER]")
            print(f"URL: {url}")
            print(f"METHOD: PUT")
            print(f"BODY: {data}")

            response = requests.put(url, json=data)

            print(f"\n[SERVER -> CLIENT RESPONSE]")
            print(f"STATUS: {response.status_code}")
            print(f"RAW TEXT: {response.text}\n")

            return response.json()
        except Exception as e:
            print("REST error:", e)
            return None


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
