import socket
import ssl


SERVER_HOST = "localhost"
SERVER_PORT = 6543

CERT_FILE = "certificates/server_b.crt"


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
    
def save_server_certificate(host: str, port: int, filename: str = "certificates/received_server.crt") -> None:
    """
    Retrieve the certificate presented by the TLS server
    and save it as a PEM .crt file.
    """
    certificate = ssl.get_server_certificate(
        (host, port)
    )

    with open(filename, "w") as file:
        file.write(certificate)

    print(f"[+] Server certificate saved to: {filename}")
    
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
        save_server_certificate(SERVER_HOST, SERVER_PORT, "certificates/received_server.crt")
        context = create_ssl_context_verify()
        connect_to_server(context) #crt verfication 1
        rc = 1
    except FileNotFoundError:
        print("[-] certificates/server_b.crt was not found")
    except ConnectionRefusedError:
        print("[-] Connection refused. Start server.py first.")
    except ssl.SSLCertVerificationError as error: 
        #2
        print(f"[-] Certificate verification failed: {error}")
        result = input("Your connection isn't private, would you like to proceed with no certificate verification? enter yes or no: ")
        if result == "yes":
            context = create_ssl_context_no_verify() #connect with no crt verification
            try:
                connect_to_server(context) #3
                rc = 1
            except Exception as e:
                print("Error:", e)
        
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
