import socket
import threading
import argparse
import struct


class SocketClient:
    def __init__(self, server_ip: str, port: int):
        self.server_ip = server_ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sequential_id = -1

    def connect(self):
        try:
            self.client.connect((self.server_ip, self.port))
            print(f"[+] Connected to {self.server_ip}:{self.port}")
            #self.client.sendall(b"hi this is tit milk")
            with open("handshake_msg.bin", "rb") as f:
                lines = f.readlines()
            for line in lines:                
                self.client.sendall(line)
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
                self.save_msg_to_file(message)                                
                # reprint prompt
                #print("Enter amount of money you want: ", end="", flush=True)

            except:
                print("\n[!] Error receiving data")
                break
    
    def read_msg_from_file(self, file_id_p):
        lines = []
        if file_id_p == 0:
            with open("amount_msg.bin", "rb") as f:
                lines = f.readlines()
        elif file_id_p == 1:
            with open("handshake_msg.bin", "rb") as f:
                lines = f.readlines()
        return lines

    def send_message(self):
        try:
            lines = self.read_msg_from_file(0)
            for line in lines:
                self.client.sendall(line)
            lines = self.read_msg_from_file(1)
            for line in lines:                
                self.client.sendall(line)
        except Exception as e:
            print(f"[!] Error sending message: {e}")
            
    def save_msg_to_file(self, msg_p):
        self.sequential_id +=1
        with open(f"output//{self.sequential_id}_s_to_c_msg.bin", "wb") as f:
            f.write(msg_p.encode())

    """
    def request_money_loop(self):
        while True:
            amount = input("Enter amount of money you want: ")

            if amount.lower() in ["exit", "quit"]:
                print("Closing connection...")
                self.client.close()
                break

            # send amount
            #self.send_message(amount)

            # confirmation
            #print(f"This is your requested money: {amount}")
    """
    def run(self):
        self.connect()

        # start receiving thread
        threading.Thread(target=self.receive_messages, daemon=True).start()

        # ONLY run money request loop
        while True:
            input("")
            self.send_message()


def main():
    parser = argparse.ArgumentParser(description="Socket Client")
    parser.add_argument("--ip", required=True, help="Server IP address")
    parser.add_argument("--port", type=int, default=9000, help="Server port")

    args = parser.parse_args()

    client = SocketClient(args.ip, args.port)
    client.run()


if __name__ == "__main__":
    main()