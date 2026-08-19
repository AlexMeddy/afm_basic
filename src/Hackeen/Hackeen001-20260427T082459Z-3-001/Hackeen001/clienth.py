import socket
import threading
import argparse
import struct


class SocketClient:
    def __init__(self, server_ip: str, port: int):
        self.server_ip = server_ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client.connect((self.server_ip, self.port))
            print(f"[+] Connected to {self.server_ip}:{self.port}")
            self.client.sendall(b"hi this is tit milk")
        except Exception as e:
            print(f"[!] Connection failed: {e}")
            exit()

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if not message:
                    print("\n[!] Server disconnected")
                    break

                # Move cursor to new line and overwrite prompt cleanly
                print("\r" + " " * 60, end="")   # clear current line
                print("\r", end="")              # return to start

                print(f"[SERVER]: {message}")

                # reprint prompt
                print("Enter amount of money you want: ", end="", flush=True)

            except:
                print("\n[!] Error receiving data")
                break
                    

    def send_message(self, message: str):
        try:
            amount = int(message)
            self.client.sendall(b"hi this is tit milk")
            data = struct.pack("!I", amount)
            print(f"[SENDING RAW]: {data}")
            self.client.sendall(data)
        except Exception as e:
            print(f"[!] Error sending message: {e}")

    def request_money_loop(self):
        """Continuously ask for money and send it"""
        while True:
            amount = input("Enter amount of money you want: ")

            if amount.lower() in ["exit", "quit"]:
                print("Closing connection...")
                self.client.close()
                break

            # send amount
            self.send_message(amount)

            # confirmation
            #print(f"This is your requested money: {amount}")

    def run(self):
        self.connect()

        # start receiving thread
        threading.Thread(target=self.receive_messages, daemon=True).start()

        # ONLY run money request loop
        self.request_money_loop()


def main():
    parser = argparse.ArgumentParser(description="Socket Client")
    parser.add_argument("--ip", required=True, help="Server IP address")
    parser.add_argument("--port", type=int, default=9000, help="Server port")

    args = parser.parse_args()

    client = SocketClient(args.ip, args.port)
    client.run()


if __name__ == "__main__":
    main()