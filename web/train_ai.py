import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

print("Bắt đầu đọc dữ liệu và huấn luyện AI...")

# 1. Đọc dữ liệu từ file CSV
df = pd.read_csv('smart_home_data.csv')

# 2. Tách dữ liệu thành: Input (X) và Output (y)
# Input: Giờ, Ánh sáng, Mưa
X = df[['Hour', 'Light', 'IsRaining']]
# Output: Trạng thái đèn (0 hoặc 1)
y = df['LightStatus']

# Chia dữ liệu: 80% để học (train), 20% để kiểm tra (test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Khởi tạo mô hình AI (Decision Tree)
model = DecisionTreeClassifier(max_depth=4) # Giới hạn độ sâu để AI không bị "học vẹt"

# 4. Huấn luyện mô hình
model.fit(X_train, y_train)

# 5. Kiểm tra độ chính xác như đi thi
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Huấn luyện thành công! Độ chính xác của AI: {accuracy * 100:.2f}%")

# 6. Xuất mô hình ra một file .pkl để tuần sau Server.py sử dụng
joblib.dump(model, 'smart_home_model.pkl')
print("Đã lưu bộ não AI vào file 'smart_home_model.pkl'")