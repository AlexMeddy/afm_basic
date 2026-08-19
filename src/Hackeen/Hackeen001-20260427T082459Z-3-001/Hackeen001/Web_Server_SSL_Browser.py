import socket
import ssl
import os


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


def handle_client(client: ssl.SSLSocket) -> None:

    request = client.recv(4096).decode(errors="ignore")

    print(request)

    if not request:
        return

    request_line = request.split("\r\n")[0]

    method, path, version = request_line.split(" ")

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
        keyfile=KEY_FILE
    )

    return context


def start_server() -> None:

    ssl_context = create_ssl_context()

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))

    server.listen()

    print(f"HTTPS server running at https://localhost:{PORT}")

    while True:

        client_socket, address = server.accept()

        print(f"TCP connection from {address}")

        try:

            ssl_client = ssl_context.wrap_socket(
                client_socket,
                server_side=True
            )

            print(f"TLS connection established with {address}")

            handle_client(ssl_client)

            ssl_client.close()

        except ssl.SSLError as error:

            print("SSL error:", error)

            client_socket.close()


start_server()