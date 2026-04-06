/* main.js */
async function refreshData() {
  try {
    const response = await fetch("http://192.168.0.106:5000/api/sensor");
    if (!response.ok) throw new Error("Lỗi kết nối");
    const data = await response.json();

    // 1 & 2. Nhiệt độ và Độ ẩm
    const tempEl = document.getElementById('temperature');
    tempEl.innerText = data.temperature + '°C';
    tempEl.className = 'value ' + (data.temperature > 30 ? 'status-danger' : 'status-safe');
    document.getElementById('humidity').innerText = data.humidity + '%';

    // 3. Ánh sáng (Lấy từ mạch thật)
    document.getElementById('light').innerText = data.light + ' raw';

    // 4. Trạng thái Mưa (Lấy từ mạch thật)
    const rainEl = document.getElementById('rain');
    rainEl.innerText = data.isRaining ? 'Có Mưa' : 'Trời Tạnh';
    rainEl.className = 'value ' + (data.isRaining ? 'status-danger' : 'status-safe');

    // 5. Cửa sổ (Logic tự động: Đóng ngay lập tức nếu có mưa)
    const doorEl = document.getElementById('door');
    const doorIcon = document.getElementById('doorIcon');
    const isDoorClosed = data.isRaining; // Tự đóng khi mưa
    
    doorEl.innerText = isDoorClosed ? 'Đóng' : 'Mở';
    doorEl.className = 'value ' + (isDoorClosed ? 'status-safe' : 'status-warning');
    doorIcon.className = isDoorClosed ? 'fa-solid fa-door-closed' : 'fa-solid fa-door-open';

    // 5. Đèn phòng: Được điều khiển hoàn toàn bởi Trí tuệ nhân tạo (AI)
    const lightEl = document.getElementById('lightStatus');
    const lightIcon = document.getElementById('lightBulbIcon');
    
    // Đọc quyết định từ AI thay vì logic cứng
    const isLightOn = data.ai_light_status === 1; 
    
    lightEl.innerText = isLightOn ? 'ON (AI Auto)' : 'OFF (AI Auto)';
    lightEl.className = 'value ' + (isLightOn ? 'status-warning' : 'status-safe');
    if(lightIcon) lightIcon.style.color = isLightOn ? '#f59e0b' : '#9ca3af';

    // Giàn phơi đồ: Thu vào nếu trời mưa
    const clotheslineEl = document.getElementById('clothesline');
    if (data.isRaining) {
        clotheslineEl.innerText = "Đã thu vào";
        clotheslineEl.className = 'value status-warning';
    } else {
        clotheslineEl.innerText = "Đang phơi";
        clotheslineEl.className = 'value status-safe';
    }

  } catch (error) {
    console.error("Không thể lấy dữ liệu từ ESP32:", error);
  }
}

window.onload = refreshData;
setInterval(refreshData, 5000); // Tự động cập nhật mỗi 5 giây