import socket
import threading
import argparse


def receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(f"[SERVER] {data.decode()}")
        except:
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server-ip", required=True)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.server_ip, args.port))

    print(f"[+] Connected to {args.server_ip}:{args.port}")

    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    while True:
        msg = input("[CLIENT SEND] ")
        sock.sendall(msg.encode())


if __name__ == "__main__":
    main()