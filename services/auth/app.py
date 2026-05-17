from flask import Flask, request, jsonify
import time, random, os
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('auth_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('auth_request_duration_seconds', 'Request latency')

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "auth"})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/auth/login', methods=['POST'])
@REQUEST_LATENCY.time()
def login():
    data = request.get_json()
    if not data or 'username' not in data:
        REQUEST_COUNT.labels('POST', '/auth/login', '400').inc()
        return jsonify({"error": "Missing credentials"}), 400
    # Simulate auth
    token = f"token-{data['username']}-{int(time.time())}"
    REQUEST_COUNT.labels('POST', '/auth/login', '200').inc()
    return jsonify({"token": token, "user": data['username']})

@app.route('/auth/validate', methods=['POST'])
def validate():
    data = request.get_json()
    token = data.get('token', '')
    if token.startswith('token-'):
        REQUEST_COUNT.labels('POST', '/auth/validate', '200').inc()
        return jsonify({"valid": True})
    REQUEST_COUNT.labels('POST', '/auth/validate', '401').inc()
    return jsonify({"valid": False}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
