# Internet Speed Dashboard

A simple and responsive web dashboard to monitor internet download speed in real time.

This application lets you monitor your internet connection speed every minute, displaying results on an interactive chart.

## Features
- **No backend scheduler:** The backend does not run speedtests on its own. Speedtests are performed only when requested by the frontend (on page load, via countdown timer, or manual button click).
- **Python Flask backend:** Exposes two endpoints:
  - `POST /speedtest` — triggers a speedtest and stores the result in memory.
  - `GET /history` — returns the list of results from the last 24 hours (up to 1440 entries).
- **Frontend (HTML + Chart.js):**
  - Responsive and mobile-friendly dashboard.
  - Line chart with real-time updates showing download speed (Mbps) over time.
  - Manual speedtest button.
  - Automatic speedtest every minute, triggered by a countdown timer in the frontend.
  - Countdown timer and info box with last update time.
  - Button and timer are always in sync with backend state.
  - Error handling: if a speedtest fails, the UI recovers gracefully and shows a clear error message.
- **Data storage:** Results are kept only in RAM (no persistent database).
- **Modern UX:** Loading indicators, error messages, and a clean, simple design.

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the backend:
   ```bash
   python app.py
   ```
3. Open your browser at [http://localhost:5000/](http://localhost:5000/)

## Project Structure

```
.
├── app.py                # Flask backend
├── requirements.txt      # Python dependencies
├── static/
│   └── index.html        # Frontend (HTML, JS, CSS)
└── README.md             # Project documentation
```

## Notes
- The backend stores results only in memory (data will be lost after restart).
- The backend never runs speedtests unless triggered by a frontend request.
- The chart shows the download speed in Mbps measured every minute (or on manual request).
- All logic for scheduling, countdown, and UI feedback is managed by the frontend.
