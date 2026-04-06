#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "NBD";
const char* password = "12345689";

const char* serverName = "http://192.168.0.106:5000/api/sensor";

#define LIGHT_PIN 34
#define RAIN_PIN 35

void setup() {
  Serial.begin(115200);
  pinMode(LIGHT_PIN, INPUT);
  pinMode(RAIN_PIN, INPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    int rawLight = analogRead(LIGHT_PIN);
    bool isRaining = (digitalRead(RAIN_PIN) == LOW);

    String json = "{";
    json += "\"temperature\":0.0,";
    json += "\"humidity\":0.0,";
    json += "\"light\":" + String(rawLight) + ",";
    json += "\"isRaining\":" + String(isRaining ? "true" : "false");
    json += "}";

    int httpResponseCode = http.POST(json);
    
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    
    http.end();
  }
  
  delay(2000);
}