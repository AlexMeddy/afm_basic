import socket
import threading


def receive_messages(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[CLIENT → SERVER] {data.decode()}")
        except:
            break


def main():
    host = "0.0.0.0"
    port = 8000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)

    print(f"[+] Server listening on {host}:{port}")

    conn, addr = server.accept()
    print(f"[+] Client connected from {addr}")

    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()

    while True:
        msg = input("[SERVER SEND] ")
        conn.sendall(msg.encode())


if __name__ == "__main__":
    main()