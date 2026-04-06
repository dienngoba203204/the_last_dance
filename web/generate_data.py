import pandas as pd
import random

# Tạo danh sách chứa dữ liệu
data = []

print("Đang tạo 5000 dòng dữ liệu thói quen giả lập...")

for _ in range(5000):
    # Tạo ngẫu nhiên giờ trong ngày (0 - 23)
    hour = random.randint(0, 23)
    
    # Tạo ngẫu nhiên mức độ ánh sáng (0 - 4095)
    light = random.randint(0, 4095)
    
    # Tạo ngẫu nhiên trạng thái mưa (0: Không mưa, 1: Có mưa)
    # Tỉ lệ mưa là khoảng 20%
    is_raining = 1 if random.random() < 0.2 else 0
    
    # --- LOGIC THÓI QUEN NGƯỜI DÙNG (Để AI học) ---
    light_status = 0 # Mặc định là tắt đèn (0)
    
    # Ban đêm (từ 18h tối đến 5h sáng) -> Đa số bật đèn
    if hour >= 18 or hour <= 5:
        light_status = 1
    # Ban ngày nhưng trời tối đen (light > 3000, do module của bạn số càng cao càng tối) -> Bật đèn
    elif light > 3000:
        light_status = 1
    # Ban ngày, trời mưa râm mát (light > 2000) -> Thường bật đèn
    elif is_raining == 1 and light > 2000:
        light_status = 1
        
    # Thêm 5% nhiễu (ngẫu nhiên) để mô hình AI học thực tế hơn, không bị máy móc cứng nhắc
    if random.random() < 0.05:
        light_status = 1 - light_status # Lật trạng thái
        
    data.append([hour, light, is_raining, light_status])

# Lưu ra file CSV
df = pd.DataFrame(data, columns=['Hour', 'Light', 'IsRaining', 'LightStatus'])
df.to_csv('smart_home_data.csv', index=False)
print("Đã tạo xong file 'smart_home_data.csv'!")