# Tác giả: Ngo Ba Dien
# Chức năng: Huấn luyện AI Dự báo thời tiết IoT

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

print("Đang đọc dữ liệu và huấn luyện AI Dung hợp (Sensor Fusion)...")

# 1. Nạp dữ liệu
df = pd.read_csv('sensor_fusion_data.csv')

# 2. Tách Input (X) và Output (y)
X = df[['Temperature', 'Humidity', 'Pressure', 'Light', 'Cloudiness', 'API_Rain']]
y = df['Predict_Rain']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Huấn luyện mô hình (Giới hạn độ sâu = 5 để chống over-fitting)
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 4. Kiểm tra sức mạnh mô hình
y_pred = model.predict(X_test)
print(f"✅ Huấn luyện thành công! Độ chính xác của AI: {accuracy_score(y_test, y_pred) * 100:.2f}%\n")

# 5. Phân tích "Tâm lý" của AI (In ra Feature Importance)
print("📊 MỨC ĐỘ QUAN TRỌNG CỦA CÁC THÔNG SỐ ĐẦU VÀO:")
features = X.columns
importances = model.feature_importances_
for f, imp in zip(features, importances):
    print(f" - {f}: {imp*100:.1f}%")

# 6. Xuất xưởng
joblib.dump(model, 'smart_home_model.pkl')
print("\n✅ Đã lưu bộ não AI mới vào 'smart_home_model.pkl' (Ghi đè bản cũ thành công).")