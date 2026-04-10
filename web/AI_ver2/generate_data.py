# Tác giả: Ngo Ba Dien
# Chức năng: Tạo tập dữ liệu Sensor Fusion (6 thông số)

import pandas as pd
import random

print("Đang tạo 5000 dòng dữ liệu thời tiết (Sensor Fusion)...")
data = []

for _ in range(5000):
    # 1. TẠO THÔNG SỐ LOCAL (Từ ESP32)
    temp = round(random.uniform(20.0, 40.0), 1)
    hum = round(random.uniform(40.0, 100.0), 1)
    
    # Áp suất bình thường khoảng 1010-1015 hPa. Áp thấp (dễ mưa) thường < 1005 hPa
    pres = round(random.uniform(990.0, 1025.0), 1)
    light = random.randint(0, 4095)
    
    # 2. TẠO THÔNG SỐ CLOUD (Từ API)
    cloudiness = random.randint(0, 100)
    api_rain = 1 if random.random() < 0.3 else 0 # Giả lập 30% API dự báo có mưa

    # 3. LOGIC "TRỜI MƯA" ĐỂ DẠY AI (Khoa học dữ liệu)
    predict_rain = 0 # Mặc định là không mưa
    
    # Quy luật 1: Áp thấp nhiệt đới (Áp suất < 1005) + Độ ẩm cao (> 85%) -> Chắc chắn mưa cục bộ
    if hum > 85 and pres < 1005:
        predict_rain = 1
    # Quy luật 2: Mây mù bao phủ (> 80%) và API báo mưa -> Mưa diện rộng
    elif api_rain == 1 and cloudiness > 80:
        predict_rain = 1
    # Quy luật 3: Độ ẩm bão hòa (> 95%) dù áp suất bình thường -> Vẫn mưa (mưa rào)
    elif hum > 95:
        predict_rain = 1

    # 4. Tiêm nhiễu chủ động (5%) để AI không bị học vẹt
    if random.random() < 0.05:
        predict_rain = 1 - predict_rain

    data.append([temp, hum, pres, light, cloudiness, api_rain, predict_rain])

# Xuất ra file Excel (CSV)
df = pd.DataFrame(data, columns=['Temperature', 'Humidity', 'Pressure', 'Light', 'Cloudiness', 'API_Rain', 'Predict_Rain'])
df.to_csv('sensor_fusion_data.csv', index=False)
print("✅ Đã xuất file 'sensor_fusion_data.csv' thành công!")