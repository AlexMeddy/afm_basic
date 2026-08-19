import socket

HOST = "127.0.0.1"
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"[+] Sending to {HOST}:{PORT}")

while True:
    message = input("Enter message: ")

    client.sendto(message.encode(), (HOST, PORT))

    if message.lower() == "quit":
        break

client.close()