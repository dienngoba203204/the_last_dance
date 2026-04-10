const serverUrl = "http://192.168.0.102:5000";

async function refreshData() {
  try {
    const response = await fetch(`${serverUrl}/api/sensor`); 
    if (!response.ok) throw new Error(`Lỗi kết nối: ${response.status}`);
    const data = await response.json();

    // 1. DỮ LIỆU ĐẦU VÀO
    document.getElementById('temperature').innerText = (data.temperature !== undefined ? data.temperature.toFixed(1) : '--') + '°C';
    document.getElementById('humidity').innerText = (data.humidity !== undefined ? data.humidity.toFixed(1) : '--') + '%';
    if (data.pressure !== undefined) document.getElementById('pressure').innerText = data.pressure.toFixed(1) + ' hPa';
    document.getElementById('light').innerText = data.light !== undefined ? data.light : '--';
    
    // Cloud API & Rain Local
    if (data.cloudiness !== undefined) document.getElementById('cloudiness').innerText = data.cloudiness + '%';
    const rainEl = document.getElementById('rain');
    rainEl.innerText = data.isRaining ? 'Có Mưa' : 'Tạnh Ráo';
    rainEl.className = 'value ' + (data.isRaining ? 'status-danger' : 'status-safe');

    // 2. AI PHÂN TÍCH
    const aiRainEl = document.getElementById('aiPredictRain');
    const isAiPredictingRain = data.ai_predict_rain === 1;
    aiRainEl.innerText = isAiPredictingRain ? 'SẮP CÓ MƯA' : 'QUANG MÂY';
    aiRainEl.className = 'value ' + (isAiPredictingRain ? 'status-danger' : 'status-safe');

    const aiLightEl = document.getElementById('aiPredictLight');
    const isAiLightOn = data.ai_light_status === 1;
    aiLightEl.innerText = isAiLightOn ? 'BẬT ĐÈN' : 'TẮT ĐÈN';
    aiLightEl.className = 'value ' + (isAiLightOn ? 'status-warning' : 'status-safe');

    // 3. THIẾT BỊ THỰC THI (Dựa trên quyết định của AI)
    // Cửa & Giàn phơi phụ thuộc vào ai_predict_rain (Chủ động thu trước khi mưa)
    const doorEl = document.getElementById('door');
    doorEl.innerText = isAiPredictingRain ? 'Đóng (Bảo vệ)' : 'Mở';
    doorEl.className = 'value ' + (isAiPredictingRain ? 'status-safe' : 'status-warning');
    document.getElementById('doorIcon').className = isAiPredictingRain ? 'fa-solid fa-door-closed' : 'fa-solid fa-door-open';

    const clotheslineEl = document.getElementById('clothesline');
    clotheslineEl.innerText = isAiPredictingRain ? "Đã thu vào" : "Đang phơi";
    clotheslineEl.className = 'value ' + (isAiPredictingRain ? 'status-warning' : 'status-safe');

    // Đèn phụ thuộc vào ai_light_status
    const lightStatusEl = document.getElementById('lightStatus');
    lightStatusEl.innerText = isAiLightOn ? 'ON (AI Auto)' : 'OFF (AI Auto)';
    lightStatusEl.className = 'value ' + (isAiLightOn ? 'status-warning' : 'status-safe');
    document.getElementById('lightBulbIcon').style.color = isAiLightOn ? '#f59e0b' : '#9ca3af';

    // 4. POPUP HUMAN-IN-THE-LOOP
    if (data.suggestion && data.suggestion.show === true) {
        showChatbotPopup(data.suggestion.message);
    }

  } catch (error) {
    console.error("Lỗi:", error);
  }
}

// HÀM ĐIỀU KHIỂN POPUP
function showChatbotPopup(message) {
  const popup = document.getElementById('aiPopup');
  if (popup && popup.style.display === 'none') {
    document.getElementById('aiMessage').innerText = message;
    popup.style.display = 'block';
  }
}
function hidePopup() { document.getElementById('aiPopup').style.display = 'none'; }
function acceptSuggestion() { alert("Đang gửi lệnh thực thi..."); hidePopup(); }
function startVoiceAuth() { alert("Đang kích hoạt Micro..."); hidePopup(); }

window.onload = refreshData;
setInterval(refreshData, 2000);