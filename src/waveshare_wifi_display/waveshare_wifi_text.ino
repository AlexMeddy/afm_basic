// TCP text receiver for the Waveshare ESP32-Touch-LCD-3.5
// The computer sends one UTF-8 line to TCP port 5000. The text is drawn on
// the built-in ST7796 display. This uses the classic ESP32/WROOM-32 pinout.

#include <Arduino_GFX_Library.h>
#include <WiFi.h>
#include <Wire.h>
#include "TCA9554.h"

// Replace these with your Wi-Fi network details.
const char *WIFI_SSID = "bonitao";
const char *WIFI_PASSWORD = "123alex123";

static const uint16_t TCP_PORT = 5000;
static const size_t MAX_MESSAGE_BYTES = 300;
static const int GFX_BL = 25;

// Waveshare ESP32-Touch-LCD-3.5 display connection.
TCA9554 ioExpander(0x20);
Arduino_DataBus *displayBus = new Arduino_ESP32SPI(
    27 /* DC */, 5 /* CS */, 18 /* SCK */, 23 /* MOSI */, 19 /* MISO */);
Arduino_GFX *gfx = new Arduino_ST7796(
    displayBus, GFX_NOT_DEFINED /* RST */, 0 /* rotation */, true /* IPS */);

WiFiServer server(TCP_PORT);

void showStatus(const String &line1, const String &line2 = "") {
  gfx->fillScreen(RGB565_BLACK);
  gfx->setTextWrap(true);
  gfx->setTextSize(2);
  gfx->setTextColor(RGB565_CYAN);
  gfx->setCursor(8, 8);
  gfx->println(line1);
  if (line2.length()) {
    gfx->setTextColor(RGB565_WHITE);
    gfx->println(line2);
  }
}

void showMessage(const char *message) {
  // Keep the connection details at the top and replace the previous message.
  gfx->fillRect(0, 72, gfx->width(), gfx->height() - 72, RGB565_BLACK);
  gfx->setTextWrap(true);
  gfx->setTextSize(2);
  gfx->setTextColor(RGB565_WHITE);
  gfx->setCursor(8, 82);
  gfx->print(message);
}

void drawConnectedScreen() {
  gfx->fillScreen(RGB565_BLACK);
  gfx->setTextWrap(true);
  gfx->setTextSize(2);
  gfx->setTextColor(RGB565_CYAN);
  gfx->setCursor(8, 8);
  gfx->println("Wi-Fi message display");
  gfx->setTextColor(RGB565_WHITE);
  gfx->print("IP: ");
  gfx->println(WiFi.localIP().toString());
  gfx->print("TCP port: ");
  gfx->println(TCP_PORT);
  gfx->println("Waiting for a message...");
}

void handleClient(WiFiClient &client) {
  char message[MAX_MESSAGE_BYTES + 1];
  size_t length = 0;
  bool tooLong = false;
  const uint32_t startedAt = millis();

  // The sender terminates each message with a newline.
  while (millis() - startedAt < 10000) {
    while (client.available()) {
      int value = client.read();
      if (value < 0) break;
      char c = (char)value;
      if (c == '\n') goto message_complete;
      if (c == '\r') continue;
      if (length < MAX_MESSAGE_BYTES) {
        message[length++] = c;
      } else {
        tooLong = true;
      }
    }
    if (!client.connected() && !client.available()) break;
    delay(2);
  }

message_complete:
  message[length] = '\0';
  if (!length) {
    client.println("ERROR: empty message");
  } else if (tooLong) {
    client.println("ERROR: message is over 300 bytes");
  } else {
    Serial.printf("Message received (%u bytes): %s\n",
                  (unsigned int)length, message);
    showMessage(message);
    client.println("OK: displayed");
  }
  client.flush();
  client.stop();
}

void setup() {
  Serial.begin(115200);
  delay(250);

  // Reset/enable the display using the onboard I/O expander.
  Wire.begin(21, 22);  // SDA, SCL for the classic ESP32-Touch-LCD-3.5
  ioExpander.begin();
  ioExpander.pinMode1(0, OUTPUT);
  ioExpander.write1(0, 1);
  delay(10);
  ioExpander.write1(0, 0);
  delay(10);
  ioExpander.write1(0, 1);
  delay(200);

  if (!gfx->begin()) {
    Serial.println("Display initialization failed.");
    while (true) delay(1000);
  }
  pinMode(GFX_BL, OUTPUT);
  digitalWrite(GFX_BL, HIGH);
  showStatus("Starting Wi-Fi...");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.printf("Connecting to Wi-Fi: %s\n", WIFI_SSID);

  const uint32_t wifiStartedAt = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - wifiStartedAt < 30000) {
    delay(500);
    Serial.print('.');
  }
  Serial.println();

  if (WiFi.status() != WL_CONNECTED) {
    showStatus("Wi-Fi did not connect", "Check the name/password and use 2.4 GHz Wi-Fi.");
    Serial.println("Wi-Fi connection timed out. Check the credentials and 2.4 GHz network.");
    return;
  }

  server.begin();
  server.setNoDelay(true);
  drawConnectedScreen();
  Serial.printf("Connected. Board IP: %s\n", WiFi.localIP().toString().c_str());
  Serial.printf("Listening for TCP messages on port %u\n", TCP_PORT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    delay(100);
    return;
  }

  WiFiClient client = server.available();
  if (client) {
    Serial.printf("Sender connected: %s\n", client.remoteIP().toString().c_str());
    handleClient(client);
  }
  delay(2);
}
