from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)


api_key = os.environ.get('API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form.get('text')
    voice = request.form.get('voice', 'banmai')
    speed = request.form.get('speed', 0)

    
    if not api_key:
        return jsonify({"error": "API key chưa được cấu hình."}), 500

    url = "https://api.fpt.ai/hmi/tts/v5"
    headers = {
        "api_key": api_key,
        "voice": voice,
        "speed": str(speed),
        "Content-Type": "application/json; charset=utf-8",  
    }
    data = {
        "text": text.strip()  
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        if result.get("async"):
            return jsonify({"audio_url": result["async"]})
        else:
            return jsonify({"error": "Không có liên kết âm thanh trả về."}), 400
    else:
        return jsonify({"error": "Lỗi khi gửi yêu cầu."}), response.status_code

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
