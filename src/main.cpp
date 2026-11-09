#include <Arduino.h>
#include <Wire.h>
#include "MAX30105.h"

// MAX30102 -> ESP32
// VCC/VIN -> 3V3, GND -> GND, SDA -> GPIO21, SCL -> GPIO22

MAX30105 sensor;
uint32_t sampleIndex = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);

  if (!sensor.begin(Wire, I2C_SPEED_STANDARD)) {
    Serial.println("# ERROR: MAX30102 not found. Check wiring and power.");
    while (true) {
      delay(1000);
    }
  }

  // LED current, averaging=1 (no FIFO averaging), Red+IR, 100 samples/s,
  // LED pulse width=411 us, ADC range=4096 nA.
  sensor.setup(0x1F, 1, 2, 100, 411, 4096);
  Serial.println("sample,red,ir");
}

void loop() {
  // Read all pending Red/IR ADC samples from the sensor FIFO.
  sensor.check();
  while (sensor.available()) {
    const uint32_t red = sensor.getFIFORed();
    const uint32_t ir = sensor.getFIFOIR();
    Serial.printf("%lu,%lu,%lu\n",
                  static_cast<unsigned long>(sampleIndex++),
                  static_cast<unsigned long>(red),
                  static_cast<unsigned long>(ir));
    sensor.nextSample();
  }
}
