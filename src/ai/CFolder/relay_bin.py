import socket
import threading
import argparse
#python relay_bin.py --server-ip 127.0.0.1 --server-port 62432 --client-ip 0.0.0.0 --client-port 2000

class RelayApp:
    def __init__(self, server_ip, server_port, client_ip, client_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_ip = client_ip
        self.client_port = client_port

        self.server_conn = None
        self.client_conn = None

    # STEP 1: connect to remote server FIRST
    def connect_to_server(self):
        try:
            self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_conn.connect((self.server_ip, self.server_port))
            print(f"[+] Connected to server {self.server_ip}:{self.server_port}")
        except Exception as e:
            print(f"[!] Failed to connect to server: {e}")
            exit(1)

    # STEP 2: start listening for client AFTER server connection
    def start_client_listener(self):
        try:
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listener.bind((self.client_ip, self.client_port))
            listener.listen(1)

            print(f"[+] Waiting for client on {self.client_ip}:{self.client_port}...")
            self.client_conn, addr = listener.accept()
            print(f"[+] Client connected from {addr}")
        except Exception as e:
            print(f"[!] Client listener error: {e}")
            exit(1)

    def handle_client_to_server(self):
        while True:
            try:
                data = self.client_conn.recv(4096)
                if not data:
                    break

                # HEX PRINT
                print(f"[CLIENT -> SERVER] HEX: {data.hex()}")

                # (optional readable text)
                #print(f"[CLIENT -> SERVER] TEXT: {data.decode(errors='ignore')}")

                self.server_conn.sendall(data)

            except Exception as e:
                print(f"[!] Error (client -> server): {e}")
                break


    def handle_server_to_client(self):
        while True:
            try:
                data = self.server_conn.recv(4096)
                if not data:
                    break

                # HEX PRINT
                print(f"[SERVER -> CLIENT] HEX: {data.hex()}")

                # (optional readable text)
                #print(f"[SERVER -> CLIENT] TEXT: {data.decode(errors='ignore')}")

                self.client_conn.sendall(data)

            except Exception as e:
                print(f"[!] Error (server -> client): {e}")
                break

    def start(self):
        self.connect_to_server()
        self.start_client_listener()

        t1 = threading.Thread(target=self.handle_client_to_server)
        t2 = threading.Thread(target=self.handle_server_to_client)

        t1.start()
        t2.start()

        t1.join()
        t2.join()


def main():
    parser = argparse.ArgumentParser(description="Socket Relay App")

    # server (remote)
    parser.add_argument("--server-ip", required=True, help="Server IP")
    parser.add_argument("--server-port", type=int, required=True, help="Server Port")

    # client (local listener)
    parser.add_argument("--client-ip", default="0.0.0.0", help="Client bind IP")
    parser.add_argument("--client-port", type=int, default=65432, help="Client port")

    args = parser.parse_args()

    app = RelayApp(
        args.server_ip,
        args.server_port,
        args.client_ip,
        args.client_port
    )

    app.start()


if __name__ == "__main__":
    main()