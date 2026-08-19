import socket
import struct

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


HOST = "127.0.0.1"
PORT = 65432


def send_message(sock: socket.socket, data: bytes) -> None:
    """
    Send a length-prefixed application-layer message.

    Format:
        4-byte message length
        message bytes
    """
    header = struct.pack("!I", len(data))
    sock.sendall(header + data)


def receive_exactly(sock: socket.socket, length: int) -> bytes:
    data = bytearray()

    while len(data) < length:
        chunk = sock.recv(length - len(data))

        if not chunk:
            raise ConnectionError("Connection closed before all data arrived.")

        data.extend(chunk)

    return bytes(data)


def receive_message(sock: socket.socket) -> bytes:
    header = receive_exactly(sock, 4)
    message_length = struct.unpack("!I", header)[0]
    return receive_exactly(sock, message_length)


def load_public_key(public_key_bytes: bytes):
    return serialization.load_pem_public_key(public_key_bytes)


def encrypt_message(public_key, plaintext: bytes) -> bytes:
    return public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def connect_to_server(host: str, port: int) -> socket.socket:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket


def main():
    with connect_to_server(HOST, PORT) as client_socket:
        print("Connected to server.")

        public_key_bytes = receive_message(client_socket)

        print("Received server public key:")
        print(public_key_bytes.decode("utf-8"))

        server_public_key = load_public_key(public_key_bytes)

        plaintext = b"This message was encrypted at Layer 7."
        encrypted_message = encrypt_message(server_public_key, plaintext)

        print("Plaintext:", plaintext.decode("utf-8"))
        print(f"Ciphertext: {len(encrypted_message)} bytes")
        print(encrypted_message.hex())

        send_message(client_socket, encrypted_message)

        response = receive_message(client_socket)
        print("Server response:", response.decode("utf-8"))


if __name__ == "__main__":
    main()