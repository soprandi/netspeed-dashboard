import threading
import time
import json
import random
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
import speedtest

app = Flask(__name__)

# In-memory storage for speed test results
data_history = []
lock = threading.Lock()

# Rate limiting protection
last_test_time = 0
MIN_INTERVAL_BETWEEN_TESTS = 30  # seconds

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Configurable: how many minutes to keep (24h = 1440)
MAX_HISTORY = 1440


def run_speedtest():
    global last_test_time
    
    # Rate limiting: ensure minimum interval between tests
    current_time = time.time()
    if current_time - last_test_time < MIN_INTERVAL_BETWEEN_TESTS:
        time.sleep(MIN_INTERVAL_BETWEEN_TESTS - (current_time - last_test_time))
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Running speedtest (attempt {attempt + 1}/{max_retries})...")
            st = speedtest.Speedtest()
            
            # Configure to look more like a regular browser
            st.get_best_server()
            
            # Add random delay to avoid pattern detection
            time.sleep(random.uniform(1, 3))
            
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            print(f"Download speed: {download_speed} Mbps")
            
            last_test_time = time.time()
            return round(download_speed, 2)
            
        except Exception as e:
            print(f"Speedtest error (attempt {attempt + 1}): {e}")
            
            # If we get a 403, wait longer before next attempt
            if "403" in str(e) or "forbidden" in str(e).lower():
                wait_time = 60 * (attempt + 1)  # Progressive backoff
                print(f"Rate limit detected, waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                # For other errors, wait a bit before retry
                time.sleep(5)
            
            if attempt == max_retries - 1:
                print("All retry attempts failed")
                return None
    
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
