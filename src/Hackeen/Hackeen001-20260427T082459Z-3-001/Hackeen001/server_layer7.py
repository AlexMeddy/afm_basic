import socket
import struct

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


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


def generate_private_key():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )


def get_public_key(private_key):
    return private_key.public_key()


def convert_public_key_to_bytes(public_key) -> bytes:
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def decrypt_message(private_key, encrypted_message: bytes) -> bytes:
    return private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def create_server_socket(host: str, port: int) -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    return server_socket


def handle_client(client_socket: socket.socket, private_key, public_key_bytes: bytes) -> None:
    send_message(client_socket, public_key_bytes)
    print("Sent server public key.")

    encrypted_message = receive_message(client_socket)

    print(f"Received ciphertext: {len(encrypted_message)} bytes")
    print(encrypted_message.hex())

    plaintext = decrypt_message(private_key, encrypted_message)
    print("Decrypted message:", plaintext.decode("utf-8"))

    response = b"Server successfully decrypted your message."
    send_message(client_socket, response)


def main():
    private_key = generate_private_key()
    public_key = get_public_key(private_key)
    public_key_bytes = convert_public_key_to_bytes(public_key)

    with create_server_socket(HOST, PORT) as server_socket:
        print(f"Server listening on {HOST}:{PORT}")

        client_socket, client_address = server_socket.accept()

        with client_socket:
            print(f"Client connected: {client_address}")
            handle_client(client_socket, private_key, public_key_bytes)


if __name__ == "__main__":
    main()