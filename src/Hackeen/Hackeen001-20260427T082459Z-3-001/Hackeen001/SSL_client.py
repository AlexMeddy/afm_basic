import socket
import ssl


SERVER_HOST = "localhost"
SERVER_PORT = 6543

CERT_FILE = "server.crt"


def create_ssl_context() -> ssl.SSLContext:
    """
    Create a client TLS context.

    server.crt is trusted as the server's certificate authority
    for this local simulation.
    """
    context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH
    )
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

    return context


def send_message(sock: ssl.SSLSocket, data: bytes) -> None:
    """
    Send application data through the encrypted TLS connection.
    """
    sock.sendall(data)


def receive_message(sock: ssl.SSLSocket) -> bytes:
    """
    Receive up to 4096 decrypted application bytes.
    """
    return sock.recv(4096)


def connect_to_server() -> None:
    """
    Create a TCP connection and then establish TLS over it.
    """
    context = create_ssl_context()
    print("before context ", context)
    with socket.create_connection(
        (SERVER_HOST, SERVER_PORT)
    ) as tcp_socket:
        with context.wrap_socket(
            tcp_socket,
            server_hostname=SERVER_HOST,
        ) as tls_socket:
            #tls_socket = context.wrap_socket(tcp_socket,server_hostname=SERVER_HOST)
            print("[+] TLS connection established")
            print(f"[+] TLS version: {tls_socket.version()}")
            print(f"[+] Cipher: {tls_socket.cipher()}")

            message = input("Enter a message: ")

            send_message(
                tls_socket,
                message.encode("utf-8"),
            )

            response = receive_message(tls_socket)

            if response:
                print(f"[SERVER] {response.decode('utf-8')}")
            else:
                print("[-] Server closed the connection")


def main() -> None:
    try:
        connect_to_server()
    except FileNotFoundError:
        print("[-] server.crt was not found")
    except ConnectionRefusedError:
        print("[-] Connection refused. Start server.py first.")
    except ssl.SSLCertVerificationError as error:
        print(f"[-] Certificate verification failed: {error}")
    except ssl.SSLError as error:
        print(f"[-] TLS error: {error}")
    except KeyboardInterrupt:
        print("\n[+] Client stopped")


if __name__ == "__main__":
    main()