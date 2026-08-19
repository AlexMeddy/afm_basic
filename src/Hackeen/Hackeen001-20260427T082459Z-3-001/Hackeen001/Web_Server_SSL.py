import socket
import os
import ssl

HOST = "127.0.0.1"
PORT = 8443

WEB_ROOT = "pages"
CERT_FILE = "server.crt"
KEY_FILE = "server.key"


def get_file_path(request_path: str) -> str:
    """
    Convert a URL path into a file path.

    /        -> pages/index.html
    /about   -> pages/about.html
    """

    if request_path == "/":
        request_path = "/index.html"

    elif "." not in request_path:
        request_path += ".html"

    request_path = request_path.lstrip("/")

    return os.path.join(WEB_ROOT, request_path)


def get_content_type(file_path: str) -> str:
    """
    Return the MIME type for common web files.
    """

    if file_path.endswith(".html"):
        return "text/html"

    if file_path.endswith(".css"):
        return "text/css"

    if file_path.endswith(".js"):
        return "application/javascript"

    if file_path.endswith(".png"):
        return "image/png"

    if file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
        return "image/jpeg"

    return "application/octet-stream"


def receive_http_request(client: ssl.SSLSocket) -> bytes:
    """
    Receive a complete HTTP request from an already-decrypted TLS socket.

    TLS records and TCP packets may be split into several pieces, so do not
    assume one recv() call contains the complete HTTP request.
    """

    data = b""

    # First receive until the complete HTTP header has arrived.
    while b"\r\n\r\n" not in data:
        chunk = client.recv(4096)
        
        if not chunk:
            return data

        data += chunk
    header_data, body = data.split(b"\r\n\r\n", 1)

    # Find Content-Length if the request contains a body, such as a POST.
    content_length = 0

    for line in header_data.split(b"\r\n"):
        if line.lower().startswith(b"content-length:"):
            content_length = int(line.split(b":", 1)[1].strip())
            break

    # Keep receiving until the complete HTTP body has arrived.
    while len(body) < content_length:
        chunk = client.recv(4096)

        if not chunk:
            break

        body += chunk

    return header_data + b"\r\n\r\n" + body


def handle_client(client: ssl.SSLSocket) -> None:
    request_bytes = receive_http_request(client)
    print("request_bytes: ", request_bytes)
    if not request_bytes:
        return

    # At this point TLS has already decrypted the encrypted network data.
    request = request_bytes.decode(errors="ignore")

    print("\n----- DECRYPTED HTTP REQUEST -----")
    print(request)
    print("----------------------------------")

    request_line = request.split("\r\n")[0]

    parts = request_line.split(" ")

    if len(parts) != 3:
        print("[-] Invalid HTTP request line:", request_line)
        return

    method, path, version = parts

    print("Method:", method)
    print("Path:", path)
    print("Version:", version)

    file_path = get_file_path(path)
    print("File:", file_path)

    if os.path.isfile(file_path):

        with open(file_path, "rb") as file:
            body = file.read()

        header = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {get_content_type(file_path)}\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        client.sendall(header.encode() + body)

    else:

        body = b"<h1>404 Not Found</h1>"

        header = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        client.sendall(header.encode() + body)


def create_ssl_context() -> ssl.SSLContext:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    context.load_cert_chain(
        certfile=CERT_FILE,
        keyfile=KEY_FILE,
    )

    return context


def start_server() -> None:
    context = create_ssl_context()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )

        server_socket.bind((HOST, PORT))
        server_socket.listen(5)

        print(f"[+] HTTPS server listening at https://{HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"\n[+] TCP connection from {client_address}")

            try:
                ssl_client = context.wrap_socket(
                    client_socket,
                    server_side=True,
                )

                print(f"[+] TLS connection established with {client_address}")

                with ssl_client:
                    handle_client(ssl_client)

            except ssl.SSLError as error:
                print("[-] SSL error:", error)
                client_socket.close()

            except (ConnectionResetError, BrokenPipeError) as error:
                print("[-] Connection error:", error)
                client_socket.close()


def main() -> None:
    try:
        start_server()
    except FileNotFoundError:
        print("[-] server.crt or server.key was not found")
    except KeyboardInterrupt:
        print("\n[+] Server stopped")


if __name__ == "__main__":
    main()