import socket
import threading

HOST = "127.0.0.1"   # change to server IP if needed
PORT = 2012          # change to your server port


def receive_messages(sock):
    buffer = ""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Disconnected from server")
                break

            buffer += data.decode()

            while "\n" in buffer:
                msg, buffer = buffer.split("\n", 1)
                print(f"\n[RECV] {msg}")

        except Exception as e:
            print("Receive error:", e)
            break


def send_messages(sock):
    while True:
        try:
            msg = input()
            sock.sendall((msg + "\n").encode())
        except Exception as e:
            print("Send error:", e)
            break


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")
    except Exception as e:
        print("Connection failed:", e)
        return

    # start receiving thread
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    # main thread handles sending
    send_messages(sock)


if __name__ == "__main__":
    main()