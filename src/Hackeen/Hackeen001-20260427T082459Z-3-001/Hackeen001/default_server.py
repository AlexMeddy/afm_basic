import socket

HOST = "127.0.0.1"
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(1)

print(f"[*] Listening on {HOST}:{PORT}")

client, addr = server.accept()
print(f"[+] Connected by {addr}")

while True:
    data = client.recv(1024)

    if not data:
        print("[!] Client disconnected")
        break

    print(f"Received: {data.decode()}")

client.close()
server.close()