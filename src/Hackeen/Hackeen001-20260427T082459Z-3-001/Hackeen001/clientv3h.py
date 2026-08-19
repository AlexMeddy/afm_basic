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
            handshake = self.caesar_encode("hi this is tit milk")
            self.socket_client.sendall(handshake.encode())
            print(f"[socket_client SENT]: {handshake}")
        except Exception as e:
            print(f"[!] Connection failed: {e}")
            exit()

    def receive_messages(self):
        #while True:
        try:
            raw = self.socket_client.recv(1024)

            if not raw:
                print("\n[!] Server disconnected")
                #break
            print(f"[SERVER]: {raw}")

        except Exception as e:
            print(f"\n[!] Error receiving data: {e}")
            #break
    
    def read_msg_from_file(self, file_id_p):
        binary_msg = None
        if file_id_p == 0:
            with open("amount_msg.bin", "rb") as f:
                binary_msg = f.read()
        elif file_id_p == 1:
            with open("handshake_msg.bin", "rb") as f:
                binary_msg = f.read()
        return binary_msg
        
    def caesar_encode(self, text, shift=3):
        result = ""
        for char in text:
            if 'a' <= char <= 'z':
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += char
        return result
        
    def caesar_decode(self, text, shift=3):
        return self.caesar_encode(text, -shift)

    def send_message(self, binary_msg_p):
        try:            
            self.socket_client.sendall(binary_msg_p)            
        except Exception as e:
            print(f"[!] Error sending message: {e}")
            
    def save_msg_to_file(self, msg_p):
        self.sequential_id +=1
        with open(f"output//{self.sequential_id}_s_to_c_msg.bin", "wb") as f:
            f.write(msg_p.encode())
            
    def print_hi(self):
        while True:
            print("hi")
            time.sleep(5)

    """
    def request_money_loop(self):
        while True:
            amount = input("Enter amount of money you want: ")

            if amount.lower() in ["exit", "quit"]:
                print("Closing connection...")
                self.socket_client.close()
                break

            # send amount
            #self.send_message(amount)

            # confirmation
            #print(f"This is your requested money: {amount}")
    """
    def run(self):
        self.connect()

        # start receiving thread
        #threading.Thread(target=self.receive_messages, daemon=True).start()
        threading.Thread(target=self.print_hi, daemon=True).start() #2
        # ONLY run money request loop
        while True:
            input("")
            self.receive_messages() #3 recv
            response = self.caesar_encode("TITMILK00")
            self.socket_client.sendall(response.encode())
            binary_msg = self.read_msg_from_file(0)
            self.send_message(binary_msg)
            #print("binary_msg type: ", type(binary_msg))
            binary_msg = self.read_msg_from_file(1) #1 read
            #print(binary_msg)
            binary_msg = binary_msg.decode()
            binary_msg = self.caesar_encode(binary_msg)
            binary_msg = binary_msg.encode()
            self.send_message(binary_msg) #2 send


def main():
    parser = argparse.ArgumentParser(description="Socket socket_client")
    parser.add_argument("--ip", required=True, help="Server IP address")
    parser.add_argument("--port", type=int, default=9000, help="Server port")

    args = parser.parse_args()

    socket_client = Socketsocket_client(args.ip, args.port)
    socket_client.run()


if __name__ == "__main__":
    main()