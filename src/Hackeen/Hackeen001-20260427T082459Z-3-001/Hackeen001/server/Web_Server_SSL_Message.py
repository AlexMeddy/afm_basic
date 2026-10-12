import socket
import ssl


SERVER_HOST = "localhost"
SERVER_PORT = 6543
CERT_FILE = "certificates/server_b.crt"
KEY_FILE = "certificates/server_b.key"


def create_ssl_context() -> ssl.SSLContext:
    """Load the certificate and private key used by the TLS server."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    return context


def handle_client(client: ssl.SSLSocket, address) -> None:
    """Receive one message and send a response over the TLS connection."""
    try:
        message = client.recv(4096)
        if not message:
            print(f"Client {address} closed without sending a message")
            return

        decoded = message.decode("utf-8", errors="replace")
        print(f"[{address}] {decoded}")
        client.sendall(f"Server received: {decoded}".encode("utf-8"))
    except OSError as error:
        print(f"Connection with {address} ended: {error}")
    finally:
        client.close()


def start_server() -> None:
    ssl_context = create_ssl_context()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((SERVER_HOST, SERVER_PORT))
        server.listen()
        print(f"TLS message server listening on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            tcp_socket, address = server.accept()
            try:
                tls_client = ssl_context.wrap_socket(tcp_socket, server_side=True)
                print(f"TLS connection established with {address}")
                handle_client(tls_client, address)
            except OSError as error:
                # Clients may connect only to fetch the certificate, then close
                # during the handshake or before sending an application message.
                print(f"Connection from {address} ended during TLS setup: {error}")
                tcp_socket.close()


if __name__ == "__main__":
    start_server()
