#include <Arduino.h>

const int pin = 25;

void setup() {
  Serial.begin(115200);
  pinMode(pin, OUTPUT);
  digitalWrite(pin, HIGH);  // 初期状態をHIGHに設定
  Serial.println("GPIO25 initialized HIGH");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // 改行や空白を除去

    if (input.equalsIgnoreCase("HIGH")) {
      digitalWrite(pin, HIGH);
      Serial.println("GPIO25 -> HIGH");
    } 
    else if (input.equalsIgnoreCase("LOW")) {
      digitalWrite(pin, LOW);
      Serial.println("GPIO25 -> LOW");
    } 
    else {
      Serial.println("Unknown command. Use 'HIGH' or 'LOW'.");
    }
  }
}
