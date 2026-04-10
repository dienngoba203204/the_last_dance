#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

// 1. CẤU HÌNH WI-FI & SERVER
const char* ssid = "NBD";
const char* password = "12345689";
const char* serverName = "http://192.168.0.102:5000/api/sensor";

// 2. CẤU HÌNH CÁC CHÂN CẢM BIẾN
#define LIGHT_PIN 34      // Chân A0 của cảm biến ánh sáng
#define RAIN_PIN 35       // Chân D0 của cảm biến mưa

// Khởi tạo đối tượng BME280 (Giao tiếp I2C mặc định SDA=21, SCL=22)
Adafruit_BME280 bme; 

void setup() {
  Serial.begin(115200);
  
  pinMode(LIGHT_PIN, INPUT);
  pinMode(RAIN_PIN, INPUT);

  // Khởi động BME280. Địa chỉ I2C của module thường là 0x76. 
  // (Nếu báo lỗi không tìm thấy cảm biến, hãy thử đổi 0x76 thành 0x77)
  unsigned status = bme.begin(0x76); 
  if (!status) {
    Serial.println("Cảnh báo: Không tìm thấy cảm biến BME280, hãy kiểm tra lại dây nối!");
  } else {
    Serial.println("Khởi động BME280 thành công!");
  }

  // Kết nối Wi-Fi
  Serial.print("Đang kết nối WiFi: ");
  Serial.println(ssid);
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

    // 1. ĐỌC BME280
    float t = bme.readTemperature();
    float h = bme.readHumidity();
    float p = bme.readPressure() / 100.0F; // Chia 100 để đổi từ đơn vị Pa sang hPa

    // Xử lý lỗi mượt mà nếu cảm biến lỏng dây
    if (isnan(t)) t = 0.0;
    if (isnan(h)) h = 0.0;
    if (isnan(p)) p = 0.0;

    // 2. ĐỌC ÁNH SÁNG & MƯA
    int rawLight = analogRead(LIGHT_PIN);
    bool isRaining = (digitalRead(RAIN_PIN) == LOW);

    // 3. TẠO CHUỖI JSON (Đã thêm thông số áp suất - pressure)
    String json = "{";
    json += "\"temperature\":" + String(t) + ",";
    json += "\"humidity\":" + String(h) + ",";
    json += "\"pressure\":" + String(p) + ",";
    json += "\"light\":" + String(rawLight) + ",";
    json += "\"isRaining\":" + String(isRaining ? "true" : "false");
    json += "}";

    // 4. GỬI LÊN PYTHON SERVER
    int httpResponseCode = http.POST(json);
    
    Serial.print("Đã gửi dữ liệu - Nhiệt độ: ");
    Serial.print(t);
    Serial.print("C | HTTP Code: ");
    Serial.println(httpResponseCode); // In ra 200 là thành công
    
    http.end();
  }
  
  delay(2000); // 2 giây gửi 1 lần
}