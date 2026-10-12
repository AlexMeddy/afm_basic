"""Send one line of text over Wi-Fi to the Waveshare ESP32 display."""

from __future__ import annotations

import socket
import sys


PORT = 5000
MAX_MESSAGE_BYTES = 300


def main() -> int:
    if len(sys.argv) < 3:
        print('Usage: py send_message.py <board-ip> "message text"')
        return 2

    host = sys.argv[1]
    payload = " ".join(sys.argv[2:]).encode("utf-8")
    if not payload:
        print("Message cannot be empty.")
        return 2
    if len(payload) > MAX_MESSAGE_BYTES:
        print(f"Message is {len(payload)} bytes; maximum is {MAX_MESSAGE_BYTES}.")
        return 2
    if b"\n" in payload or b"\r" in payload:
        print("Use one line per message.")
        return 2

    try:
        with socket.create_connection((host, PORT), timeout=5) as connection:
            connection.settimeout(12)
            connection.sendall(payload + b"\n")
            connection.shutdown(socket.SHUT_WR)
            reply = bytearray()
            while len(reply) < 256:
                chunk = connection.recv(256 - len(reply))
                if not chunk:
                    break
                reply.extend(chunk)
                if b"\n" in chunk:
                    break
    except OSError as exc:
        print(f"Could not reach the board at {host}:{PORT}: {exc}")
        return 1

    response = reply.decode("utf-8", errors="replace").strip()
    print(response or "The board closed the connection without replying.")
    return 0 if response.startswith("OK") else 1


if __name__ == "__main__":
    raise SystemExit(main())
