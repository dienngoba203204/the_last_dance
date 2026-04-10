# File test API OpenWeatherMap
import requests
import json

# 1. Điền API Key bạn vừa đăng ký trên OpenWeatherMap vào đây
API_KEY = "dbceeef929a84fef7193cc5dfece54a3" 
CITY = "Bac Giang,VN"

def test_api():
    print(f"Đang gọi dữ liệu thời tiết cho khu vực: {CITY}...\n")
    
    # Tạo đường dẫn URL để gọi API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=vi"
    
    try:
        response = requests.get(url)
        
        # Kiểm tra xem gọi API có thành công không (Mã 200 là OK)
        if response.status_code == 200:
            data = response.json()
            
            # In toàn bộ dữ liệu ra màn hình cho đẹp dễ nhìn
            print("✅ GỌI API THÀNH CÔNG! Dưới đây là dữ liệu thô (JSON):")
            print(json.dumps(data, indent=4, ensure_ascii=False))
            
            print("\n" + "="*40 + "\n")
            
            # Trích xuất thử một vài thông số quan trọng
            print("🎯 TRÍCH XUẤT THÔNG SỐ CẦN THIẾT CHO AI:")
            print(f" - Tình trạng: {data['weather'][0]['description'].capitalize()}")
            print(f" - Nhiệt độ API báo: {data['main']['temp']} °C")
            print(f" - Độ ẩm API báo: {data['main']['humidity']} %")
            print(f" - Mây che phủ: {data['clouds']['all']} %")
            
            is_rain = "Có" if "rain" in data else "Không"
            print(f" - Dự báo có mưa không: {is_rain}")
            
        elif response.status_code == 401:
            print("❌ LỖI 401: API Key không đúng hoặc chưa được kích hoạt. (Thường API mới đăng ký cần chờ 10-15 phút mới dùng được).")
        elif response.status_code == 404:
            print("❌ LỖI 404: Không tìm thấy tên thành phố.")
        else:
            print(f"❌ LỖI KHÔNG XÁC ĐỊNH: Mã lỗi {response.status_code}")
            
    except Exception as e:
        print("❌ LỖI KẾT NỐI MẠNG:", e)

if __name__ == "__main__":
    test_api()