import threading
import time
import json
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
import speedtest

app = Flask(__name__)

# In-memory storage for speed test results
data_history = []
lock = threading.Lock()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Configurable: how many minutes to keep (24h = 1440)
MAX_HISTORY = 1440


def run_speedtest():
    try:
        print("Running speedtest...")
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        print(f"Download speed: {download_speed} Mbps")
        return round(download_speed, 2)
    except Exception as e:
        print(f"Speedtest error: {e}")
        return None



@app.route('/speedtest', methods=['POST'])
def manual_speedtest():
    speed = run_speedtest()
    timestamp = datetime.now().strftime("%H:%M")
    if speed is not None:
        with lock:
            data_history.append({"time": timestamp, "speed": speed})
            if len(data_history) > MAX_HISTORY:
                data_history.pop(0)
        return jsonify({"time": timestamp, "speed": speed}), 200
    else:
        return jsonify({"error": "Speedtest failed"}), 500

@app.route('/history', methods=['GET'])
def get_history():
    with lock:
        return jsonify(data_history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
