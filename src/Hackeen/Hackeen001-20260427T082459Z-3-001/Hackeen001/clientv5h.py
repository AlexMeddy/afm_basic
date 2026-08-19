import socket
import threading
import argparse
import struct
import time

class Socketsocket_client:
    def __init__(self, server_ip: str, port: int):
        self.server_ip = server_ip
        self.port = port
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sequential_id = -1

    def connect(self):
        try:
            self.socket_client.connect((self.server_ip, self.port))
            print(f"[+] Connected to {self.server_ip}:{self.port}")

        except Exception as e:
            print(f"[!] Connection failed: {e}")
            exit()

    def get_bla(self, name_p):
        rc = None
        return rc

    def receive_messages(self):
        raw = ""
        try:
            raw = self.socket_client.recv(1024)

            if not raw:
                print("\n[!] Server disconnected")
            print(f"[SERVER]: {raw}")
        except Exception as e:
            print(f"\n[!] Error receiving data: {e}")
        return raw
    
    def read_msg_from_file(self, filename_p):
        binary_msg = None
        with open(filename_p, "rb") as f:
            binary_msg = f.read()
        return binary_msg
        

    def send_message(self, binary_msg_p):
        try:            
            self.socket_client.sendall(binary_msg_p)            
        except Exception as e:
            print(f"[!] Error sending message: {e}")
            
    def save_msg_to_file(self, msg_p):
        self.sequential_id +=1
        with open(f"output//{self.sequential_id}_s_to_c_msg.bin", "wb") as f:
            f.write(msg_p)
            
        

def main():
    parser = argparse.ArgumentParser(description="Socket socket_client")
    parser.add_argument("--ip", required=True, help="Server IP address")
    parser.add_argument("--port", type=int, default=9000, help="Server port")

    args = parser.parse_args()

    socket_client = Socketsocket_client(args.ip, args.port)
    socket_client.connect()
    binary_msg = socket_client.read_msg_from_file("input\\0_c_to_s_msg.bin")
    socket_client.send_message(binary_msg)
    message = socket_client.receive_messages()
    socket_client.save_msg_to_file(message)
    message = socket_client.receive_messages()
    socket_client.save_msg_to_file(message)
if __name__ == "__main__":
    main()