// Basic screen test for the classic Waveshare ESP32-Touch-LCD-3.5
// (ESP32-WROOM-32). This only displays Hello World; it does not use Wi-Fi.

#include <Arduino_GFX_Library.h>
#include <Wire.h>
#include "TCA9554.h"

static const int GFX_BL = 25;

// Waveshare ESP32-Touch-LCD-3.5 display connection.
TCA9554 ioExpander(0x20);
Arduino_DataBus *displayBus = new Arduino_ESP32SPI(
    27 /* DC */, 5 /* CS */, 18 /* SCK */, 23 /* MOSI */, 19 /* MISO */);
Arduino_GFX *gfx = new Arduino_ST7796(
    displayBus, GFX_NOT_DEFINED /* RST */, 0 /* rotation */, true /* IPS */);

void setup() {
  Serial.begin(115200);

  // Reset/enable the screen using the board's built-in I/O expander.
  Wire.begin(21, 22);  // SDA, SCL
  ioExpander.begin();
  ioExpander.pinMode1(0, OUTPUT);
  ioExpander.write1(0, HIGH);
  delay(10);
  ioExpander.write1(0, LOW);
  delay(10);
  ioExpander.write1(0, HIGH);
  delay(200);

  if (!gfx->begin()) {
    Serial.println("Display initialization failed.");
    while (true) delay(1000);
  }

  pinMode(GFX_BL, OUTPUT);
  digitalWrite(GFX_BL, HIGH);

  gfx->fillScreen(RGB565_BLACK);
  gfx->setTextWrap(true);
  gfx->setTextSize(3);
  gfx->setTextColor(RGB565_WHITE);
  gfx->setCursor(20, 40);
  gfx->println("Hello World!");
}

void loop() {
  Serial.println("Hello World is displayed.");
  delay(1000);
}
