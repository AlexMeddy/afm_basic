import socket
import ssl


HOST = "127.0.0.1"
PORT = 6543

CERT_FILE = "server.crt"
KEY_FILE = "server.key"


def create_ssl_context() -> ssl.SSLContext:
    """
    Create the TLS context used by the server.

    The certificate identifies the server.
    The private key must remain on the server.
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    context.load_cert_chain(
        certfile=CERT_FILE,
        keyfile=KEY_FILE,
    )

    return context


def receive_message(sock: ssl.SSLSocket) -> bytes:
    """
    Receive up to 4096 decrypted application bytes.
    """
    return sock.recv(4096)


def send_message(sock: ssl.SSLSocket, data: bytes) -> None:
    """
    Send application data through the encrypted TLS connection.
    """
    sock.sendall(data)


def handle_client(client_socket: socket.socket, context: ssl.SSLContext) -> None:
    """
    Perform the TLS handshake and communicate with one client.
    """
    try:
        with context.wrap_socket(
            client_socket,
            server_side=True,
        ) as tls_socket:
            print("[+] TLS connection established")
            print(f"[+] TLS version: {tls_socket.version()}")
            print(f"[+] Cipher: {tls_socket.cipher()}")

            message = receive_message(tls_socket)

            if not message:
                print("[-] Client sent no data")
                return

            decoded_message = message.decode("utf-8")
            print(f"[CLIENT] {decoded_message}")

            response = f"Server received: {decoded_message}"
            send_message(tls_socket, response.encode("utf-8"))

    except ssl.SSLError as error:
        print(f"[-] TLS error: {error}")

    except UnicodeDecodeError:
        print("[-] Client sent invalid UTF-8 data")


def start_server() -> None:
    """
    Start the TCP server and wait for TLS clients.
    """
    context = create_ssl_context()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )

        server_socket.bind((HOST, PORT))
        server_socket.listen(5)

        print(f"[+] TLS server listening on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"\n[+] TCP connection from {client_address}")

            with client_socket:
                handle_client(client_socket, context)


def main() -> None:
    try:
        start_server()
    except FileNotFoundError:
        print("[-] server.crt or server.key was not found")
    except KeyboardInterrupt:
        print("\n[+] Server stopped")


if __name__ == "__main__":
    main()