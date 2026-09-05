import socket
import ssl


SERVER_HOST = "localhost"
SERVER_PORT = 6543

CERT_FILE = "server1.crt"


def create_ssl_context_verify() -> ssl.SSLContext:
    """
    Create a TLS client context that verifies the server certificate.
    """
    context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH,
        cafile=CERT_FILE,
    )

    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

    return context
    
def create_ssl_context_no_verify() -> ssl.SSLContext:
    """
    Create a client TLS context.

    server.crt is trusted as the server's certificate authority
    for this local simulation.
    
    context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH
    )
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
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


def connect_to_server(context) -> None:
    """
    Create a TCP connection and then establish TLS over it.
    """
    #rc = -1 #disconnected
    #print("before context ", context)
    with socket.create_connection(
        (SERVER_HOST, SERVER_PORT)
    ) as tcp_socket:
        with context.wrap_socket(
            tcp_socket,
            server_hostname=SERVER_HOST,
        ) as tls_socket:
            #tls_socket = context.wrap_socket(tcp_socket,server_hostname=SERVER_HOST)
            print("[+] TLS connection established")
            #rc = 1
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
    #return rc


def main() -> None:
    rc = -1
    try:
        context = create_ssl_context_verify()
        connect_to_server(context)
        rc = 1
    except FileNotFoundError:
        print("[-] server.crt was not found")
    except ConnectionRefusedError:
        print("[-] Connection refused. Start server.py first.")
    except ssl.SSLCertVerificationError as error:
        print(f"[-] Certificate verification failed: {error}")
        context = create_ssl_context_no_verify()
        connect_to_server(context)
        rc = 1
    except ssl.SSLError as error:
        print(f"[-] TLS error: {error}")
    except KeyboardInterrupt:
        print("\n[+] Client stopped")
    
    if rc == 1:
        print("i know it worked")
    else:
        print("i know it failed")
        


if __name__ == "__main__":
    main()