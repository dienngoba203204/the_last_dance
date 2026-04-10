# Tác giả: Ngo Ba Dien
# Chức năng: Server AIoT Trung Tâm - Dung hợp dữ liệu (Sensor Fusion)

from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import time
import joblib
import pandas as pd
import requests

app = Flask(__name__)
CORS(app)

# ==========================================
# 1. CẤU HÌNH API ĐÁM MÂY (OPENWEATHERMAP)
# ==========================================
API_KEY = "dbceeef929a84fef7193cc5dfece54a3"
CITY = "Bac Giang,VN"

weather_cache = {
    "cloudiness": 0, 
    "api_rain_forecast": 0, 
    "last_update": 0 
}

# ==========================================
# 2. TẢI BỘ NÃO AI DỰ BÁO THỜI TIẾT
# ==========================================
try:
    MODEL_PATH = r"C:\Users\Admin\Documents\LATN\the_last_dance\web\AI_ver2\smart_home_model.pkl"
    
    ai_weather_model = joblib.load(MODEL_PATH)
    print("✅ Đã tải mô hình AI Sensor Fusion thành công từ:", MODEL_PATH)
except Exception as e:
    print("⚠️ Cảnh báo: Không tìm thấy file model. Vui lòng kiểm tra lại đường dẫn!")
    print("Chi tiết lỗi:", e)
    ai_weather_model = None

# Biến lưu trữ trạng thái hệ thống
latest_data = {
    "temperature": 0.0,
    "humidity": 0.0,
    "pressure": 0.0,
    "light": 0,
    "isRaining": False,
    "cloudiness": 0,
    "ai_predict_rain": 0, 
    "ai_light_status": 0,
    "timestamp": "Chưa có dữ liệu",
    "suggestion": {"show": False, "message": ""} 
}

def fetch_weather_api():
    global weather_cache
    # Gọi API đám mây 15 phút/lần (900 giây) để tránh bị khóa tài khoản
    if time.time() - weather_cache["last_update"] > 900:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
            resp = requests.get(url).json()
            
            weather_cache["cloudiness"] = resp.get('clouds', {}).get('all', 0)
            weather_cache["api_rain_forecast"] = 1 if 'rain' in resp else 0
            weather_cache["last_update"] = time.time()
            
            print(f"🌤️ Đồng bộ API Cloud: Mây {weather_cache['cloudiness']}% | Dự báo mưa: {weather_cache['api_rain_forecast']}")
        except Exception as e:
            print("❌ Lỗi lấy API Thời tiết:", e)
            
    return weather_cache["cloudiness"], weather_cache["api_rain_forecast"]

# ==========================================
# 3. XỬ LÝ DỮ LIỆU & AI SUY LUẬN
# ==========================================
@app.route('/api/sensor', methods=['POST'])
def receive_data():
    global latest_data
    data = request.get_json()
    
    if data:
        # Nhận dữ liệu Local Edge
        latest_data.update(data)
        latest_data['timestamp'] = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Nhận dữ liệu Cloud
        cloud, api_rain = fetch_weather_api()
        latest_data['cloudiness'] = cloud
        
        # Lấy thông số để đưa vào Model
        temp = data.get('temperature', 0)
        hum = data.get('humidity', 0)
        pres = data.get('pressure', 0)
        light = data.get('light', 0)
        
        latest_data['suggestion'] = {"show": False, "message": ""}
        
        # --- AI BẮT ĐẦU PHÂN TÍCH ---
        if ai_weather_model:
            try:
                # Tạo bảng dữ liệu 6 thông số chuẩn xác như lúc huấn luyện
                input_df = pd.DataFrame([[temp, hum, pres, light, cloud, api_rain]], 
                                        columns=['Temperature', 'Humidity', 'Pressure', 'Light', 'Cloudiness', 'API_Rain'])
                
                # AI DỰ BÁO MƯA (0: Không mưa, 1: Sắp mưa)
                predict_rain = int(ai_weather_model.predict(input_df)[0])
                latest_data['ai_predict_rain'] = predict_rain
                
                # AI QUYẾT ĐỊNH ĐÈN (Tạm dùng logic ngưỡng cho đến khi train mô hình riêng cho đèn)
                ai_light = 1 if light > 2500 else 0
                latest_data['ai_light_status'] = ai_light
                
                # In Log ra màn hình Server để dễ quan sát
                print(f"[{latest_data['timestamp']}] Nhiệt: {temp}°C | Ẩm: {hum}% | Áp suất: {pres} hPa | AI Dự báo mưa: {'CÓ' if predict_rain == 1 else 'KHÔNG'}")

                # --- KỊCH BẢN GIAO TIẾP (HUMAN-IN-THE-LOOP) ---
                if temp > 32.0:
                    latest_data['suggestion'] = {
                        "show": True,
                        "message": f"Nhiệt độ phòng đang là {temp}°C. Bạn có muốn hệ thống tự động bật quạt không?"
                    }
                    
                if data.get("force_door") == "OPEN":
                    latest_data['suggestion'] = {
                        "show": True,
                        "message": "⚠️ CẢNH BÁO: Phát hiện yêu cầu mở cửa bất thường! Hãy đọc mật khẩu bằng giọng nói."
                    }

            except Exception as e:
                print("Lỗi hệ thống AI suy luận:", e)
                
        return jsonify({"message": "Đã lưu và phân tích"}), 200
        
    return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

@app.route('/api/sensor', methods=['GET'])
def send_data():
    return jsonify(latest_data), 200

# ==========================================
# 4. API DEMO TÌNH HUỐNG HACK CHO GIẢNG VIÊN
# ==========================================
@app.route('/api/hacker_test', methods=['GET'])
def hacker_test():
    global latest_data
    latest_data['suggestion'] = {
        "show": True,
        "message": "⚠️ PHÁT HIỆN LỆNH ĐIỀU KHIỂN TỪ XA BẤT THƯỜNG! Hệ thống đang chặn mở cửa. Vui lòng xác thực giọng nói."
    }
    return "Đã kích hoạt kịch bản chống xâm nhập thành công!"

if __name__ == '__main__':
    print("Khởi động Server AIoT (Sensor Fusion Hub)...")
    app.run(host='0.0.0.0', port=5000, debug=True)