from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import csv
from scheduler import start_scheduler
from modules.weather import capture_weather
import os

app = Flask(__name__)
CORS(app)

# 서버 시작시 스케줄러 시작
start_scheduler()

@app.route('/')
def home():
    return jsonify({"status": "Server is running"})

@app.route('/news')
def news():
    try:
        news_items = []
        with open('latest_news.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                news_items.append({
                    'section': row['Section'],
                    'number': row['Number'],
                    'title': row['Title'],
                    'link': row['Link'],
                    'timestamp': row['Timestamp']
                })
        return jsonify(news_items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/trending-csv')
def trending():
    try:
        trends = []
        with open('latest_trends.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                trends.append(row['Keyword'])
        return jsonify(trends)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather')
def weather():
    try:
        weather_dir = 'frontend/public/weather'
        # 가장 최근 날씨 이미지 파일 찾기
        weather_files = [f for f in os.listdir(weather_dir) if f.startswith('weather_') and f.endswith('.png')]
        if not weather_files:
            return jsonify({"error": "No weather image found"}), 404

        latest_file = sorted(weather_files)[-1]
        image_path = f'/weather/{latest_file}'
        return jsonify({"screenshot": image_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather/<path:filename>')
def serve_weather_image(filename):
    return send_from_directory('frontend/public/weather', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)