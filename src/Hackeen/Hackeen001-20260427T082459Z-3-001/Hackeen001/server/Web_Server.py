import socket
import os


HOST = "127.0.0.1"
PORT = 8080

WEB_ROOT = "pages"


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

    if file_path.endswith(".jpg"):
        return "image/jpeg"

    return "application/octet-stream"


def handle_client(client: socket.socket) -> None:
    request = client.recv(4096).decode(errors="ignore")

    print(request)

    if not request:
        return

    request_line = request.split("\r\n")[0]

    method, path, version = request_line.split(" ")
    print(path)

    file_path = get_file_path(path)
    print(file_path)

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


def start_server() -> None:

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))

    server.listen()

    print(f"Server running at http://{HOST}:{PORT}")

    while True:

        client, address = server.accept()

        print(f"Connection from {address}")

        handle_client(client)

        client.close()


start_server()