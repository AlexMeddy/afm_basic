# Wi-Fi messages on the Waveshare screen

This project targets the classic **Waveshare ESP32-Touch-LCD-3.5** board with an **ESP32-WROOM-32** module. It joins a 2.4 GHz Wi-Fi network and listens for one TCP text line at a time on port 5000. A received message replaces the previous message on the built-in screen.

## Arduino setup

1. In Arduino IDE, install **esp32 by Espressif Systems** from Boards Manager.
2. In Library Manager, install **GFX Library for Arduino** and **TCA9554**.
3. Open `waveshare_wifi_text.ino`.
4. Replace `YOUR_WIFI_NAME` and `YOUR_WIFI_PASSWORD` near the top of the sketch with your Wi-Fi details. Use your 2.4 GHz Wi-Fi network.
5. In **Tools > Board**, select **ESP32 Dev Module**. Connect the board with a USB data cable and choose the port that appears under **Tools > Port**.
6. Upload. Open **Tools > Serial Monitor** at **115200 baud**. The board's IP address is printed there and also shown on its display.

The sketch uses the Waveshare ESP32-Touch-LCD-3.5 pin setup: display reset through the onboard TCA9554 I/O expander, SPI display pins, and GPIO25 backlight. It needs no extra wires.

## Send a message from Windows

Open PowerShell in this folder and run:

```powershell
py .\send_message.py 192.168.1.42 "Hello from my computer"
```

Replace `192.168.1.42` with the IP shown on the board. The computer and board must be connected to the same local Wi-Fi network. The board replies `OK: displayed` when it has drawn the message.

## Notes

- Messages are limited to 300 UTF-8 bytes and must be a single line.
- The built-in font is intended for ordinary English/ASCII text; special Unicode characters may not render correctly.
- If the display stays blank, confirm the board's model is **ESP32-Touch-LCD-3.5** (not the ESP32-S3 version); their display connections differ.
