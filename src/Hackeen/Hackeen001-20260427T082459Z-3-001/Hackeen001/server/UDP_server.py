import socket

HOST = "127.0.0.1"
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print(f"[*] UDP Server listening on {HOST}:{PORT}")

while True:
    data, addr = server.recvfrom(1024)

    message = data.decode()

    print(f"[{addr}] {message}")

    if message.lower() == "quit":
        print("[!] Client disconnected")
        break

server.close()