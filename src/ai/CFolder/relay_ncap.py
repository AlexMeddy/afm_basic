import os
import threading
import time
from scapy.all import sniff, PcapWriter, conf


class PacketCapture:
    def __init__(self, port):

        self.port = port
        self.running = True

        # Fixed output folder
        self.output_dir = r"C:\Users\alexf\afm_basic\src\ai\CFolder\output_ncap"
        os.makedirs(self.output_dir, exist_ok=True)

        self.output_file = os.path.join(self.output_dir, "capture.pcap")

        self.writer = PcapWriter(
            self.output_file,
            append=True,
            sync=True
        )

        # Try to use loopback automatically if available
        self.iface = r"\Device\NPF_Loopback"
        
    def callback(self, packet):
        print(packet.summary())
        self.writer.write(packet)

    def sniff_loop(self):
        sniff(
            iface=r"\Device\NPF_Loopback",
            prn=self.callback,
            store=False
        )

    def start(self):
        print(f"[+] Capturing TCP port {self.port}")
        print(f"[+] Interface: {self.iface}")
        print(f"[+] Saving to: {self.output_file}")
        print("[+] Press CTRL+C to stop")

        t = threading.Thread(target=self.sniff_loop, daemon=True)
        t.start()

        try:
            while self.running:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n[+] Stopping capture...")
            self.running = False
            time.sleep(1)  # let sniff thread exit
            self.writer.close()
            print("[+] File saved successfully")


def main():
    port = input("Port to capture: ").strip()

    cap = PacketCapture(port)
    cap.start()


if __name__ == "__main__":
    main()