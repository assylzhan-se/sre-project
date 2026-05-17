from flask import Flask, request, jsonify
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('notification_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('notification_request_duration_seconds', 'Request latency')

notifications = []

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "notification"})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/notifications', methods=['POST'])
@REQUEST_LATENCY.time()
def send_notification():
    data = request.get_json()
    if not data or 'recipient' not in data or 'message' not in data:
        REQUEST_COUNT.labels('POST', '/notifications', '400').inc()
        return jsonify({"error": "Missing recipient or message"}), 400

    notification = {
        "id": len(notifications) + 1,
        "recipient": data['recipient'],
        "message": data['message'],
        "type": data.get('type', 'email'),
        "sent_at": time.time(),
        "status": "sent"
    }
    notifications.append(notification)
    REQUEST_COUNT.labels('POST', '/notifications', '201').inc()
    return jsonify(notification), 201

@app.route('/notifications', methods=['GET'])
def list_notifications():
    return jsonify({"notifications": notifications[-10:], "total": len(notifications)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
