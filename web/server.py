# Tác giả: Ngo Ba Dien
# Chức năng: Server trung tâm TÍCH HỢP AI

from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

# Tải mô hình AI đã huấn luyện
try:
    ai_model = joblib.load('smart_home_model.pkl')
    print("✅ Đã tải mô hình AI thành công!")
except Exception as e:
    print("❌ Lỗi: Không tìm thấy file smart_home_model.pkl. Hãy đảm bảo bạn đã chạy train_ai.py!")
    ai_model = None

latest_data = {
    "temperature": 0.0,
    "humidity": 0.0,
    "light": 0,
    "isRaining": False,
    "timestamp": "Chưa có dữ liệu",
    "ai_light_status": 0 # Thêm biến này để lưu quyết định của AI
}

@app.route('/api/sensor', methods=['POST'])
def receive_data():
    global latest_data
    data = request.get_json()
    
    if data:
        latest_data.update(data)
        
        # 1. Lấy giờ hiện tại trên máy tính
        current_hour = datetime.datetime.now().hour
        latest_data['timestamp'] = datetime.datetime.now().strftime("%H:%M:%S")
        
        # 2. Xử lý dữ liệu để đưa cho AI
        light_val = data.get('light', 0)
        is_raining_val = 1 if data.get('isRaining') else 0
        
        # 3. AI BẮT ĐẦU SUY LUẬN (DỰ ĐOÁN)
        if ai_model:
            # Tạo bảng dữ liệu đúng chuẩn như lúc dạy AI
            input_features = pd.DataFrame([[current_hour, light_val, is_raining_val]], 
                                          columns=['Hour', 'Light', 'IsRaining'])
            
            # AI đưa ra quyết định (0 là Tắt, 1 là Bật)
            prediction = ai_model.predict(input_features)[0]
            latest_data['ai_light_status'] = int(prediction)
            
            print(f"[{latest_data['timestamp']}] Ánh sáng: {light_val}, Mưa: {is_raining_val} | AI Quyết định đèn: {'BẬT' if prediction == 1 else 'TẮT'}")
            
        return jsonify({"message": "Đã lưu và phân tích"}), 200
        
    return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

@app.route('/api/sensor', methods=['GET'])
def send_data():
    return jsonify(latest_data), 200

if __name__ == '__main__':
    print("Khởi động Server AI Trung Tâm...")
    app.run(host='0.0.0.0', port=5000, debug=True)