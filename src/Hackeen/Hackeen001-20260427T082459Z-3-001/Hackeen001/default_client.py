import socket

HOST = "127.0.0.1"
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

print(f"[+] Connected to {HOST}:{PORT}")

def read_msg_from_file():
    msg = ""
    with open("test_msg.txt", "r") as f:
        msg = f.read()
    return msg
'''
while True:
    
    message = input("Enter message: ")

    if message.lower() == "quit":
        break
    '''
msg = read_msg_from_file()
input()
client.sendall(msg.encode())

client.close()