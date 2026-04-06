#include <DHT.h>

#define DHTPIN 4   

#define DHTTYPE DHT21

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  Serial.println("Đang khởi động cảm biến DHT21...");

  dht.begin();
}

void loop() {
  delay(2000);

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("Lỗi: Không thể đọc dữ liệu từ cảm biến DHT21!");
    return;
  }

  Serial.print("Nhiệt độ: ");
  Serial.print(t);
  Serial.print(" °C  |  ");
  
  Serial.print("Độ ẩm: ");
  Serial.print(h);
  Serial.println(" %");
}