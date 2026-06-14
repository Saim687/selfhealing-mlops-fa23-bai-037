import time
import requests
from prometheus_client import start_http_server, Gauge

CONFIDENCE_METRIC = Gauge('prediction_confidence_score', 'Latest prediction confidence score from Sentiment API')

def poll_app():
    while True:
        try:
            response = requests.get("http://localhost:32500/api/latest-confidence", timeout=2)
            if response.status_code == 200:
                data = response.json()
                CONFIDENCE_METRIC.set(data["confidence"])
            else:
                CONFIDENCE_METRIC.set(1.0)
        except Exception:
            CONFIDENCE_METRIC.set(1.0)
        time.sleep(5)

if __name__ == '__main__':
    start_http_server(8000)
    poll_app()
